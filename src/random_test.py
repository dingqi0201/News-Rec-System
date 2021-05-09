import pandas as pd
import numpy as np
from collections import namedtuple

Data = namedtuple('Data', ['size', 'clicked_words', 'hot_words', 'news_words', 'labels'])


# def read(file):
#     df = pd.read_table(file, sep='\t', header=None, names=['user_id', 'news_words', 'month', 'label'])
#     # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
#     df['news_words'] = df['news_words'].map(lambda x: [int(i) for i in x.split(',')])
#     return df
#
#
# def read_hot_news(file):
#     df_hot = pd.read_table(file, sep='\t', header=None, names=['news_words', 'count', 'month'])
#     # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
#     df_hot['news_words'] = df_hot['news_words'].map(lambda x: [int(i) for i in x.split(',')])
#     # print(df_hot)
#     return df_hot


def read_test(file):
    df = pd.read_table(file, sep='\t', header=None, names=['user_id', 'news_id', 'news_words', "label"])
    # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
    df['news_words'] = df['news_words'].map(lambda x: [int(i) for i in x.split(',')])
    return df


def read_history(file):
    df_his = pd.read_table(file, sep='\t', header=None, names=['user_id', 'news_id', 'news_words'])
    # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
    df_his['news_words'] = df_his['news_words'].map(lambda x: [int(i) for i in x.split(',')])
    return df_his


def read_hot_news(file):
    df_hot = pd.read_table(file, sep='\t', header=None, names=['news_id', 'news_words', 'count'])
    # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
    df_hot['news_words'] = df_hot['news_words'].map(lambda x: [int(i) for i in x.split(',')])
    # print(df_hot)
    return df_hot


def aggregate_test(df, history_df, hot_df):
    df.insert(4, 'clicked_words', 'NaN')
    # print("===========df===========\n", df)
    uid2words = dict()
    # print("===========uid2words===========\n", uid2words)
    for user_id in set(history_df['user_id']):
        # print("=========== set(history_df['user_id'] ===========\n", set(history_df['user_id']))
        df_user = history_df[history_df['user_id'] == user_id]
        print("=========== df_user ===========\n", df_user)
        words = np.array(df_user['news_words'].tolist())
        print("=========== words ===========\n", words)
        indices = np.random.choice(list(range(0, df_user.shape[0])), size=3,
                                   replace=True)
        print("=========== indices ===========\n", indices)
        uid2words[user_id] = words[indices]
        print("=========== uid2words[user_id] ===========\n", uid2words[user_id])
    # pd.set_option('display.max_columns', None)
    df['clicked_words'] = df['user_id'].map(lambda x: uid2words[x])
    print("===========df===========\n", df)

    # month2hot = dict()
    # for m in [3]:
    #     a_month_hot = hot_df[hot_df['month'] == m]
    #     words = np.array(a_month_hot['news_words'].tolist())
    #     indices = list(range(0, 2))
    #     print("=========== indices ===========\n", indices)
    #     month2hot[m + 1] = words[indices]  # 1月的hot写在df的2月上
    #     print("=========== month2hot ===========\n", month2hot)
    #
    # df['hot_words'] = df['month'].map(lambda x: month2hot[x])
    # # print("=========== df['hot_words'] ===========\n", df['hot_words'])

    df.insert(5, 'hot_words', 'NaN')
    words = np.array(hot_df['news_words'].tolist())
    print("==================words==================\n", words)
    indices = list(range(0, 2))
    print("==================indices==================\n", indices)
    print("==================words[indices]==================\n", words[indices])
    print("==================words[indices]==================\n", type(words[indices]))
    a = np.tile(words[indices], (10,))
    print(a)
    df['hot_words'] = a
    print("==================DF==================\n", df)
    return df


# def transform(df):  # 最终形成一个data的具名元组，包含size,clicked_words,,,labels等内容
#     # df = df.sample(frac=1).reset_index(drop=True)  # 全部行shuffle
#     # print(df)
#     data = Data(size=df.shape[0],  # 10401
#                 clicked_words=np.array(df['clicked_words'].tolist()),  # shape为（10401,30,10）
#                 hot_words=np.array(df['hot_words'].tolist()),  # (10401,15,10)
#                 news_words=np.array(df['news_words'].tolist()),  # shape为（10401,10）
#                 labels=np.array(df['label']))  # shape为（10401，）
#     # print(data)
#     return data


if __name__ == '__main__':
    test_df = read_test('../real_data/test.txt')
    print("=================== test_df =================\n", test_df)

    hot_df = read_hot_news('../real_data/hot.txt')
    print("=================== hot_df =================\n", hot_df)

    history_df = read_history('../real_data/history.txt')
    print("=================== history_df =================\n", history_df)

    test = aggregate_test(test_df, history_df, hot_df)
    print("=================== test =================\n", test)

    # test_data = transform(test)
    # print("=================== test_data =================\n", test_data)
