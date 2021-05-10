import numpy as np

MAX_TITLE_LENGTH = 29
WORD_FREQ_THRESHOLD = 1
WORD_EMBEDDING_DIM = 50
print('loading word2id map...')
# Load 读出word2id字典
word2id = np.load('app/real_data/word2id.npy').item()

def align_and_transform_for_test(file, output_file):
    """
    获取一个标题的前 MAX_TITLE_LENGTH个字符,并将汉字转换成id.
    :param file:
    :param output_file:
    :return:
    """
    reader = open(file, encoding='utf-8')
    writer = open(output_file, 'w', encoding='utf-8')
    for line in reader:
        array = line.strip().split('\t')
        user_id = array[0]
        news_id = array[1]
        title = array[2]
        month = array[3]
        label = array[4]
        if len(title) > MAX_TITLE_LENGTH:
            title = title[0:MAX_TITLE_LENGTH]
        word_encoding = encoding_title(title)
        writer.write('%s\t%s\t%s\t%s\t%s\n' % (user_id, news_id, word_encoding, month, label))
    reader.close()
    writer.close()


def align_and_transform_for_history(file, output_file):
    """
    获取一个标题的前 MAX_TITLE_LENGTH个字符,并将汉字转换成id.
    :param file:
    :param output_file:
    :return:
    """
    reader = open(file, encoding='utf-8')
    writer = open(output_file, 'w', encoding='utf-8')
    for line in reader:
        array = line.strip().split('\t')
        user_id = array[0]
        news_id = array[1]
        title = array[2]
        month = array[3]
        if len(title) > MAX_TITLE_LENGTH:
            title = title[0:MAX_TITLE_LENGTH]
        word_encoding = encoding_title(title)
        writer.write('%s\t%s\t%s\t%s\n' % (user_id, news_id, word_encoding, month))
    reader.close()
    writer.close()


def align_and_transform_for_hot(file, output_file):
    """
    获取一个标题的前 MAX_TITLE_LENGTH个字符。
    :param file:
    :param output_file:
    :return:
    """
    reader = open(file, encoding='utf-8')
    writer = open(output_file, 'w', encoding='utf-8')
    for line in reader:
        array = line.strip().split('\t')
        news_id = array[0]
        title = array[1]
        amount = array[2]
        month = array[3]
        if len(title) > MAX_TITLE_LENGTH:
            title = title[0:MAX_TITLE_LENGTH]
        word_encoding = encoding_title(title)
        writer.write('%s\t%s\t%s\t%s\n' % (news_id, word_encoding, amount, month))
    reader.close()
    writer.close()


def title2list(news_title):
    """
    将一个新闻标题分字并转换成列表
    :param news_title: 一个新闻标题字符串 E.g.:'2019年校领导寒假会商会召开'
    :return: 一个新闻标题按字切分的列表 ['2','0','1','9','年','校','领','导','寒','假','会','商','会','召','开']
    """
    title = []
    for i in news_title:
        title.append(i)
    # print("================title============\n",title)
    return title


def encoding_title(title):
    """
    根据 word2id 对一个标题进行编码
    :param title: 一个新闻标题
    :return: 该新闻标题的字编码
    """
    array = title2list(title)
    word_encoding = ['0'] * MAX_TITLE_LENGTH

    point = 0
    for s in array:
        if s in word2id:
            word_encoding[point] = str(word2id[s])
        else:
            word_encoding[point] = str(0)

        point += 1

        if point == MAX_TITLE_LENGTH:
            break
    word_encoding = ','.join(word_encoding)  # 元素用逗号分隔
    return word_encoding


# if __name__ == '__main__':
def transform_words_to_id():
    print('transforming real word to id ...')
    align_and_transform_for_test('app/real_data/raw_test.txt', 'app/real_data/raw_test_aligned_encoding.txt')
    align_and_transform_for_history('app/real_data/raw_history.txt', 'app/real_data/raw_history_aligned_encoding.txt')
    align_and_transform_for_hot('app/real_data/raw_hot.txt', 'app/real_data/raw_hot_aligned_encoding.txt')
