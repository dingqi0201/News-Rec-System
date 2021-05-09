import tensorflow as tf
import argparse
from sklearn.metrics import roc_auc_score
from data_loader import load_data

import sys
sys.path.append("../real_data")
from realnews_preprocess import transform_words_to_id


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

# parser.add_argument('--d_a_size', type=int, default=20, help='number of the hidden unit for self-attention')
# parser.add_argument('--r_size', type=int, default=3, help='number of different parts to be extracted from the news')
# parser.add_argument('--p_coef', type=float, default=0.3, help='coefficient of the penalization term P')
# parser.add_argument('--d', type=int, default=1, help='the half size of the window for CNN')
# parser.add_argument('--n_windows', type=int, default=10,
#                     help='number of windows,should be in accordance with the slide step')
parser.add_argument('--max_click_history', type=int, default=20,
                    help='number of sampled click history for each user')  # 必须设置为20，因为模型固定为.ckpt文件时该参数为20
parser.add_argument('--max_hot_news', type=int, default=3,
                    help='number of sampled hot news for each month')  # 必须设置为3，因为模型已经固定.ckpt文件时该参数为3
# parser.add_argument('--n_filters', type=int, default=8, help='number of filters for each size in KCNN')  # 原128
# parser.add_argument('--filter_sizes', type=int, default=[1, 2, 3], nargs='+',
#                     help='list of filter sizes, e.g., --filter_sizes 2 3')
# parser.add_argument('--l2_weight', type=float, default=0.01, help='weight of l2 regularization')
# parser.add_argument('--lr', type=float, default=0.01, help='learning rate')  # 原0.001
parser.add_argument('--batch_size', type=int, default=10,
                    help='number of samples in one batch')  # 可以表示计算test中前多少条候选新闻的点击概率
# parser.add_argument('--n_epochs', type=int, default=100, help='number of training epochs')

# parser.add_argument('--word_dim', type=int, default=50,
#                     help='dimension of word embeddings, please ensure that the specified input file exists')
# parser.add_argument('--max_title_length', type=int, default=29,
#                     help='maximum length of news titles, should be in accordance with the input datasets')  # 原来默认为10

# 通过argpaser对象的parser_args函数来获取所有参数args
args = parser.parse_args()


def get_feed_dict(data, start, end):
    feed_dict = {clicked_words: data.clicked_words[start:end],
                 hot_words: data.hot_words[start:end],
                 news_words: data.news_words[start:end],
                 labels: data.labels[start:end]}
    return feed_dict


""" 截取标题并将汉字转换成id """
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
feed_dict = get_feed_dict(test_data, 0, args.batch_size)
labels, scores = sess.run([labels, op_scores], feed_dict)
auc = roc_auc_score(y_true=labels, y_score=scores)
print(auc, scores)

sess.close()

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
