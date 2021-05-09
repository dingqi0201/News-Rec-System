from dhr import DHR
import tensorflow as tf
import numpy as np
import time


def get_feed_dict(model, data, start, end):
    feed_dict = {model.clicked_words: data.clicked_words[start:end],
                 model.hot_words: data.hot_words[start:end],
                 model.news_words: data.news_words[start:end],
                 model.labels: data.labels[start:end]}
    return feed_dict


def train(args, train_data, test_data):
    model = DHR(args)

    saver = tf.train.Saver(max_to_keep=1)

    # 开启会话
    with tf.Session() as sess:
        # 初始化变量
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())

        max_test_auc = 0
        step = 0
        stop = False
        require_improvement = 10
        test_f1_follow = 0

        while step < args.n_epochs and stop == False:
            # training
            # 生成从0到train_data.size（10401）的数字并按照args.batch_size的等间隔选取组成列表。
            start_list = list(range(0, train_data.size, args.batch_size))
            # 随机打乱list序列，然后从其中取batch_size大小的index元素来feed进model
            np.random.shuffle(start_list)
            max_batch_test_auc = 0
            batch_test_f1_follow = 0
            for start in start_list:
                end = start + args.batch_size
                loss, opt = model.train(sess, get_feed_dict(model, train_data, start, end))
               # print("loss: %.4f" % loss)
                if start_list.index(start) % 50 == 0:
                    # evaluation2 分batch评估test集（验证集）
                    start_list3 = list(range(0, test_data.size, args.batch_size))
                    gap_test_auc = 0
                    gap_test_f1 = 0
                    for start3 in start_list3:
                        end3 = start3 + args.batch_size
                        batch_test_auc, batch_test_f1 = model.eval(sess, get_feed_dict(model, test_data, start3, end3))
                        if start3 != start_list3[-1]:
                            gap_test_auc += batch_test_auc * (args.batch_size / test_data.size)  # 乘数量权重
                            gap_test_f1 += batch_test_f1 * (args.batch_size / test_data.size)
                        else:
                            gap_test_auc += batch_test_auc * ((test_data.size % args.batch_size) / test_data.size)  # 乘数量权重
                            gap_test_f1 += batch_test_f1 * ((test_data.size % args.batch_size) / test_data.size)                            

                    #print('epoch %d    batch_%d_test_auc: %.4f' % (step, start_list.index(start), gap_test_auc))
                    print('epoch %d    batch_%d_test_auc: %.4f    test_f1: %.4f' % (step, start_list.index(start), gap_test_auc, gap_test_f1))

                    if gap_test_auc > max_batch_test_auc:
                        max_batch_test_auc = gap_test_auc
                        batch_test_f1_follow = gap_test_f1
            # evaluation
            # train_auc = model.eval(sess, get_feed_dict(model, train_data, 0, train_data.size))
            # test_auc = model.eval(sess, get_feed_dict(model, test_data, 0, test_data.size))
            # print('epoch %d    train_auc: %.4f    test_auc: %.4f' % (step, train_auc, test_auc))

            # evaluation2 分batch评估test集（验证集）
            start_list2 = list(range(0, test_data.size, args.batch_size))
            test_auc = 0
            test_f1 = 0
            for start in start_list2:
                end = start + args.batch_size
                batch_test_auc, batch_test_f1 = model.eval(sess, get_feed_dict(model, test_data, start, end))
                if start != start_list2[-1]:
                    test_auc += batch_test_auc * (args.batch_size / test_data.size)  # 乘数量权重
                    test_f1 += batch_test_f1 * (args.batch_size / test_data.size)  # 乘数量权重
                else:
                    test_auc += batch_test_auc * ((test_data.size % args.batch_size) / test_data.size)  # 乘数量权重
                    test_f1 += batch_test_f1 * ((test_data.size % args.batch_size) / test_data.size)  # 乘数量权重

            #print('epoch %d    final_test_auc: %.4f' % (step, test_auc))
            print('epoch %d    final_test_auc: %.4f    final_test_f1: %.4f' % (step, test_auc, test_f1))


            if test_auc > max_batch_test_auc:
                max_batch_test_auc = test_auc
                batch_test_f1_follow = test_f1
            #print('epoch %d    test_auc: %.4f' % (step, max_batch_test_auc))
            print('epoch %d    test_auc: %.4f    test_f1: %.4f' % (step, max_batch_test_auc, batch_test_f1_follow))


            # 保存最佳模型的auc值
            if max_batch_test_auc > max_test_auc:
                max_test_auc = max_batch_test_auc
                best_step = step
                test_f1_follow = batch_test_f1_follow
                saver.save(sess, '../model/best-model.ckpt', global_step=step)

            else:
                # 超过10轮未产生更佳模型，触发early stopping
                if step - best_step >= require_improvement:
                    stop = True
                    print("Early stopping is triggered at epoch {}".format(step))
            print("now, best step is epoch %d" % best_step)

            step += 1

        #print("The best model is generated at epoch {}   test_auc: {:.4f}".format(best_step, max_test_auc))
        print("The best model is generated at epoch {}   test_auc: {:.4f}   test_f1: {:.4f}".format(best_step, max_test_auc, test_f1_follow))

        # 记录最高auc到文件
        writer = open('./auc.txt', 'a')
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        writer.write(
            #'Best model    epoch {:<6d}test_auc: {:<10.4f} time: {}\n'.format(best_step, max_test_auc, t))
            'Best model    epoch {:<6d}test_auc: {:<10.4f}test_f1: {:<10.4f} time: {}\n'.format(best_step, max_test_auc, test_f1_follow, t))
        writer.close()
