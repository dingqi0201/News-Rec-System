# import argparse
# from data_loader import load_data
# from train import train
# import os
#
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"  ##指定了显卡3
#
# # argparse 是python自带的命令行参数解析包，可以用来方便地读取命令行参数
# # 用argparse包中的ArgumentParser类生成一个parser对象
# parser = argparse.ArgumentParser()
# # 通过对象的add_argument()函数来增加参数
# parser.add_argument('--train_file', type=str, default='../data/raw_train.txt', help='path to the training file')
# parser.add_argument('--test_file', type=str, default='../data/raw_test.txt', help='path to the test file')
# parser.add_argument('--history_file', type=str, default='../data/history.txt', help='path to the history file')
# parser.add_argument('--hot_news_file', type=str, default='../data/raw_hot_news_lastweek.txt', help='path to the hot news file')
# # parser.add_argument('--transform', type=bool, default=False, help='whether to transform entity embeddings')  # 原来默认为True
# # parser.add_argument('--use_context', type=bool, default=False, help='whether to use context embeddings')
# parser.add_argument('--d_a_size', type=int, default=20, help='number of the hidden unit for self-attention')
# parser.add_argument('--r_size', type=int, default=3, help='number of different parts to be extracted from the news')
# parser.add_argument('--p_coef', type=float, default=0.3, help='coefficient of the penalization term P')
# parser.add_argument('--d', type=int, default=1, help='the half size of the window for CNN')
# parser.add_argument('--n_windows', type=int, default=10, help='number of windows,should be in accordance with the slide step')
# parser.add_argument('--max_click_history', type=int, default=20,
#                     help='number of sampled click history for each user')  # 原來默认为30
# parser.add_argument('--max_hot_news', type=int, default=3, help='number of sampled hot news for each month')
# parser.add_argument('--n_filters', type=int, default=8, help='number of filters for each size in KCNN')  # 原128
# parser.add_argument('--filter_sizes', type=int, default=[1, 2, 3], nargs='+',
#                     help='list of filter sizes, e.g., --filter_sizes 2 3')
# parser.add_argument('--l2_weight', type=float, default=0.01, help='weight of l2 regularization')
# parser.add_argument('--lr', type=float, default=0.01, help='learning rate')  # 原0.001
# parser.add_argument('--batch_size', type=int, default=128, help='number of samples in one batch')  # 原128
# parser.add_argument('--n_epochs', type=int, default=100, help='number of training epochs')
# #parser.add_argument('--keep_prob', type=float, default=0.7, help='keep ratio for dropout')
# # parser.add_argument('--KGE', type=str, default='TransE',
# #                     help='knowledge graph embedding method, please ensure that the specified input file exists')
# # parser.add_argument('--entity_dim', type=int, default=50,
# #                     help='dimension of entity embeddings, please ensure that the specified input file exists')
# parser.add_argument('--word_dim', type=int, default=50,
#                     help='dimension of word embeddings, please ensure that the specified input file exists')
# parser.add_argument('--max_title_length', type=int, default=29,
#                     help='maximum length of news titles, should be in accordance with the input datasets')  # 原来默认为10
#
# # 通过argpaser对象的parser_args函数来获取所有参数args
# args = parser.parse_args()
#
# train_data, test_data = load_data(args)
#
# train(args, train_data, test_data)
