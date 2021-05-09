import tensorflow as tf
import argparse
from sklearn.metrics import roc_auc_score
from app.src.data_loader import load_data

from app.real_data.realnews_preprocess import transform_words_to_id


def load_model():
    parser = argparse.ArgumentParser()
    # 通过对象的add_argument()函数来增加参数

    parser.add_argument('--raw_test_file', type=str, default='../real_data/raw_test.txt',
                        help='path to the raw test file')
    parser.add_argument('--raw_history_file', type=str, default='../real_data/raw_history.txt',
                        help='path to the raw history file')
    parser.add_argument('--raw_hot_news_file', type=str, default='../real_data/raw_hot.txt',
                        help='path to the raw hot news file')

    parser.add_argument('--test_file', type=str, default='../real_data/raw_test_aligned_encoding.txt',
                        help='path to the test file')
    parser.add_argument('--history_file', type=str, default='../real_data/raw_history_aligned_encoding.txt',
                        help='path to the history file')
    parser.add_argument('--hot_news_file', type=str, default='../real_data/raw_hot_aligned_encoding.txt',
                        help='path to the hot news file')

    parser.add_argument('--max_click_history', type=int, default=20,
                        help='number of sampled click history for each user')  # 必须设置为20，因为模型固定为.ckpt文件时该参数为20
    parser.add_argument('--max_hot_news', type=int, default=3,
                        help='number of sampled hot news for each month')  # 必须设置为3，因为模型已经固定.ckpt文件时该参数为3

    parser.add_argument('--batch_size', type=int, default=10,
                        help='number of samples in one batch')  # 可以表示计算test中前多少条候选新闻的点击概率

    # 通过argpaser对象的parser_args函数来获取所有参数args
    args = parser.parse_args()

    # 截取标题并将汉字转换成id
    transform_words_to_id(args)

    """ 加载数据；加载模型；模型计算 """
    print('loading data ... loading model ... computing ... ')

    # 加载数据
    test_data = load_data(args)

    # 加载模型
    sess = tf.Session()

    # 恢复计算图
    saver = tf.train.import_meta_graph('../model/best-model.ckpt-9.meta')
    saver.restore(sess, tf.train.latest_checkpoint("../model"))

    # 获取占位符
    graph = tf.get_default_graph()
    clicked_words = graph.get_tensor_by_name("input/clicked_words:0")
    hot_words = graph.get_tensor_by_name("input/hot_words:0")
    news_words = graph.get_tensor_by_name("input/news_words:0")
    labels = graph.get_tensor_by_name("input/labels:0")

    # 恢复scores操作
    op_scores = graph.get_tensor_by_name("Sigmoid:0")

    # 喂入数据并计算得分
    feed_dict = {clicked_words: test_data.clicked_words[0:args.batch_size],
                 hot_words: test_data.hot_words[0:args.batch_size],
                 news_words: test_data.news_words[0:args.batch_size],
                 labels: test_data.labels[0:args.batch_size]}

    labels, scores = sess.run([labels, op_scores], feed_dict)
    auc = roc_auc_score(y_true=labels, y_score=scores)
    print(auc, scores)

# sess.close()

# model = DHR(args)
# sess = load_model()
# batch_test_auc, batch_scores = model.eval(sess, get_feed_dict(model, test_data, 0, args.batch_size))
# print(batch_test_auc, batch_scores)


# sess = tf.Session()
# saver = tf.train.import_meta_graph(os.path.join("../model", 'best-model.ckpt-9.meta'))
# module_file = tf.train.latest_checkpoint("../model")
# saver.restore(sess, module_file)
# variable_names = [v.name for v in tf.trainable_variables()]
# variable_names = [v.name for v in tf.global_variables()]
# values = sess.run(variable_names)
# i = 0
# for k, v in zip(variable_names, values):
#     i += 1
#     if k.find('encode') != -1:
#         print(f"第 {i} 个variable")
#         print("Variable: ", k)
#         print("Shape: ", v.shape)
#         print(v)
# graph = tf.get_default_graph()
# all_ops = graph.get_operations()
# for el in all_ops:
#     print(el.name)
