# import argparse
import pandas as pd
import numpy as np
from collections import namedtuple
from app.real_data.realnews_preprocess import get_host_ip

def load_data():
    test_df = read('app/real_data/raw_test_aligned_encoding.txt')
    history_df = read_history('app/real_data/' + get_host_ip() +'_raw_history_aligned_encoding.txt')
    hot_df = read_hot_news('app/real_data/raw_hot_aligned_encoding.txt')
    test = aggregate_test(test_df, history_df, 20, hot_df, 3)
    test_data = transform(test)
    return test_data


def read(file):
    df = pd.read_table(file, sep='\t', header=None, names=['user_id', 'news_id', 'news_words', 'month', 'label'])
    # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
    df['news_words'] = df['news_words'].map(lambda x: [int(i) for i in x.split(',')])
    return df


def read_history(file):
    df_his = pd.read_table(file, sep='\t', header=None, names=['user_id', 'news_id', 'news_words', "month"])
    # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
    df_his['news_words'] = df_his['news_words'].map(lambda x: [int(i) for i in x.split(',')])
    return df_his


def read_hot_news(file):
    df_hot = pd.read_table(file, sep='\t', header=None, names=['news_id', 'news_words', 'count', 'month'])
    # 将news_words列的数据按照逗号所分隔的每个元素i(str类型)都转换为int类型
    df_hot['news_words'] = df_hot['news_words'].map(lambda x: [int(i) for i in x.split(',')])
    # print(df_hot)
    return df_hot


def aggregate_test(df, history_df, max_click_history, hot_df, max_hot_news):
    df.insert(5, 'clicked_words', 'NaN')
    for i in [3]:
        a_history = history_df[history_df['month'] == i]
        uid2words = dict()
        for user_id in set(a_history['user_id']):
            df_user = a_history[a_history['user_id'] == user_id]
            words = np.array(df_user['news_words'].tolist())
            indices = np.random.choice(list(range(0, df_user.shape[0])), size=max_click_history,
                                       replace=True)
            # print(indices)
            uid2words[user_id] = words[indices]

        df.loc[df['month'] == i + 1, 'clicked_words'] = df[df['month'] == i + 1]['user_id'].map(lambda x: uid2words[x])

    month2hot = dict()
    for m in [3]:
        a_month_hot = hot_df[hot_df['month'] == m]
        words = np.array(a_month_hot['news_words'].tolist())
        indices = list(range(0, max_hot_news))
        month2hot[m + 1] = words[indices]  # 3月的hot写在df的4月上
    df['hot_words'] = df['month'].map(lambda x: month2hot[x])
    # pd.set_option('display.max_columns', None)
    # print("=========== df =============\n",df)
    return df


def transform(df):  # 最终形成一个data的具名元组，包含size,clicked_words,,,labels等内容
    Data = namedtuple('Data', ['size', 'clicked_words', 'hot_words', 'news_words', 'labels'])
    data = Data(size=df.shape[0],  # 10401
                clicked_words=np.array(df['clicked_words'].tolist()),  # shape为（10401,30,10）
                hot_words=np.array(df['hot_words'].tolist()),  # (10401,15,10)
                news_words=np.array(df['news_words'].tolist()),  # shape为（10401,10）
                labels=np.array(df['label']))  # shape为（10401，）
    # print(data)
    return data
