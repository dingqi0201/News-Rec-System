# 定义DHR模型
import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score, f1_score


class DHR(object):
    def __init__(self, args):
        self.params = []  # for computing regularization loss
        self._build_inputs(args)
        self._build_model(args)
        self._build_train(args)

    def _build_inputs(self, args):
        with tf.name_scope('input'):  # 模型的输入有4个部分：用户点击过的新闻的标题对应单词、热点新闻的单词、候选集新闻的单词、label。
            # placeholder()函数是在神经网络构建graph的时候在模型中的占位，此时并没有把要输入的数据传入模型，它只会分配必要的内存。等建立session，在会话中，运行模型的时候通过feed_dict()函数向占位符喂入数据。
            self.clicked_words = tf.placeholder(
                # dtype数据类型，shape数据形状，第一维不确定(batch)，第二维长度是max_click_history，第三维长度是max_title_length。
                dtype=tf.int32, shape=[None, args.max_click_history, args.max_title_length], name='clicked_words')
            self.hot_words = tf.placeholder(
                dtype=tf.int32, shape=[None, args.max_hot_news, args.max_title_length], name='hot_words')
            self.news_words = tf.placeholder(
                dtype=tf.int32, shape=[None, args.max_title_length], name='news_words')
            self.labels = tf.placeholder(
                dtype=tf.float32, shape=[None], name='labels')
            #self.keep_prob = tf.placeholder(
                #dtype=tf.float32, name='keep_prob')

    def _build_model(self, args):
        # 得到所有单词的embedding
        with tf.name_scope('embedding'):
            word_embs = np.load('../data/word_embeddings_' + str(args.word_dim) + '.npy')
            # tf.Variable()有变量运行前必须初始化用tf.global_variables_initializer()
            self.word_embeddings = tf.Variable(word_embs, dtype=np.float32, name='word')
            self.params.append(self.word_embeddings)  # word_embeddings是词库中词的总个数*dim

        user_embeddings, news_embeddings, hot_embeddings = self._attention(args)
        """计算用户和候选之间的相似得分"""
        self.user_news_concat = tf.concat([user_embeddings, news_embeddings], axis=1)
        self.clicked_inform = tf.layers.dense(self.user_news_concat,
                                              units=args.r_size * args.n_filters * len(args.filter_sizes),
                                              activation=tf.nn.tanh)
    
        """计算热点和候选之间的相似得分"""
        self.hot_news_concat = tf.concat([hot_embeddings, news_embeddings], axis=1)
        self.hot_inform = tf.layers.dense(self.hot_news_concat,
                                          units=args.r_size * args.n_filters * len(args.filter_sizes),
                                          activation=tf.nn.tanh)
        """计算最终得分"""
        self.scores_concat = tf.concat([self.clicked_inform, self.hot_inform], axis=1)
        #只用热点不用兴趣
        #self.scores_concat = self.hot_inform
        self.scores_un = tf.layers.dense(self.scores_concat,
                                         units=args.r_size * args.n_filters * len(args.filter_sizes),
                                         activation=tf.nn.tanh)
        self.scores_unnormalized = tf.squeeze(tf.layers.dense(self.scores_un, units=1), axis=[1])
        self.scores = tf.sigmoid(self.scores_unnormalized)

        # 相加融合，系数为自动训练 add*clicked_inform + (1-add)*hot_inform
        #add = tf.get_variable(name='add_coef_clicked', shape=[1, args.r_size * args.n_filters * len(args.filter_sizes)],
                                                      #dtype=tf.float32)
        #if add not in self.params:
            #self.params.append(add)
        #one = tf.constant(1.0, shape=[1, args.r_size * args.n_filters * len(args.filter_sizes)], dtype=tf.float32)
        #sub = tf.subtract(one, add)
        #self.scores_add = tf.add(tf.multiply(add, self.clicked_inform), tf.multiply(sub, self.hot_inform))
        #self.scores_un = tf.layers.dense(self.scores_add, units = args.r_size * args.n_filters * len(args.filter_sizes),activation=tf.nn.tanh)
        #self.scores_unnormalized = tf.squeeze(tf.layers.dense(self.scores_un, units=1), axis=[1])
        #self.scores = tf.sigmoid(self.scores_unnormalized)

    # 通过attention得到user_embeddings
    def _attention(self, args):
        # (batch_size * max_click_history, max_title_length)
        # tf.reshape(tensor,shape)动态形状转换，转换前后张量的元素个数必须一致。第一个参数为修改对象，第二个参数为修改后的shape
        # shape[-1,]:-1表示我也不知道几行，
        clicked_words = tf.reshape(self.clicked_words, shape=[-1, args.max_title_length])
        hot_words = tf.reshape(self.hot_words, shape=[-1, args.max_title_length])

        with tf.variable_scope('kcnn_selfattn', reuse=tf.AUTO_REUSE):  # reuse the variables of KCNN
            # (batch_size * max_click_history 128*13, title_embedding_length)
            # title_embedding_length = r *n_filters_for_each_size * n_filter_sizes  r 跳* 每种尺寸128个核 * 2种尺寸。
            # n_filter_sizes是len(args.filter_sizes)
            clicked_embeddings = self._kcnn_selfattn(clicked_words, args)

            # (batch_size * max_hot_news 128*15, title_embedding_length)
            hot_embeddings = self._kcnn_selfattn(hot_words, args)

            # (batch_size 128, title_embedding_length)
            news_embeddings = self._kcnn_selfattn(self.news_words, args)
            # news_embeddings = self._kcnn(self.news_words, self.news_entities, args)

        # (batch_size 128, max_click_history 30, title_embedding_length)
        clicked_embeddings = tf.reshape(
            clicked_embeddings, shape=[-1, args.max_click_history, args.r_size * args.n_filters * len(args.filter_sizes)])

        # (batch_size 128, max_hot_news 15, title_embedding_length)
        hot_embeddings = tf.reshape(
            hot_embeddings, shape=[-1, args.max_hot_news, args.r_size * args.n_filters * len(args.filter_sizes)])

        # (batch_size 128, 1, title_embedding_length)
        news_embeddings_expanded = tf.expand_dims(news_embeddings, 1)

        """
        计算历史和候选之间的attention
        """
        # (batch_size 128, max_click_history 30)
        attention_weights = tf.reduce_sum(clicked_embeddings * news_embeddings_expanded,
                                          axis=-1)  # tf.reduce_sum()用于计算张量tensor沿着某一维度的和
        # ？？？我感觉没用DNN？？？
        # (batch_size 128, max_click_history 30)
        attention_weights = tf.nn.softmax(attention_weights, dim=-1)

        # (batch_size 128, max_click_history 30, 1)
        attention_weights_expanded = tf.expand_dims(attention_weights, axis=-1)

        # (batch_size 128, title_embedding_length)
        user_embeddings = tf.reduce_sum(clicked_embeddings * attention_weights_expanded, axis=1)  # 按哪个维度加和就把哪个维度消掉了

        """
        计算热点和候选之间的attention
        """
        # (batch_size 128, max_hot_news 15)
        hot_attention_weights = tf.reduce_sum(hot_embeddings * news_embeddings_expanded,
                                              axis=-1)  # tf.reduce_sum()用于计算张量tensor沿着某一维度的和
        # ？？？我感觉没用DNN？？？
        # (batch_size 128, max_hot_news 15)
        hot_attention_weights = tf.nn.softmax(hot_attention_weights, dim=-1)

        # (batch_size 128, max_hot_news 15, 1)
        hot_attention_weights_expanded = tf.expand_dims(hot_attention_weights, axis=-1)

        # (batch_size 128, title_embedding_length)
        hot_embeddings = tf.reduce_sum(hot_embeddings * hot_attention_weights_expanded, axis=1)

        #hot_embeddings = tf.reduce_mean(hot_embeddings, axis = 1)

        return user_embeddings, news_embeddings, hot_embeddings

    def _kcnn_selfattn(self, words, args):
        # (batch_size * max_click_history 128*13, max_title_length 29, word_dim 50) for users 是3维的
        # (batch_size 128, max_title_length 29, word_dim 50) for news
        embedded_words = tf.nn.embedding_lookup(self.word_embeddings,
                                                words)  # 在词库中找到一个标题中有的那些词。tf.nn.embedding_lookup函数的用法主要是选取一个张量里面索引对应的元素。tf.nn.embedding_lookup（params, ids）:params可以是张量也可以是数组等，id就是对应的索引。

        #embedded_words = tf.nn.dropout(embedded_words, keep_prob=args.keep_prob)
        with tf.name_scope("CNN"):
            # (batch_size * max_click_history, max_title_length, word_dim, 1) for users
            # (batch_size 128, max_title_length 29, word_dim 50, 1) for news
            # tf.expand_dims( ,-1)在最后增加一维
            embedded_words = tf.expand_dims(embedded_words, -1)
            # 分滑动窗口 并 拼接在一起 (滑动步长为3)
            windows = []
            for i in range(0, args.max_title_length, 3):
                if i - args.d > 0:
                    first = i - args.d
                else:
                    first = 0
                if i + args.d < args.max_title_length:
                    last = i + args.d + 1
                else:
                    last = args.max_title_length
                # (batch_size * max_click_history, 未padding的window_size, word_dim, 1) for users
                # (batch_size 128, 未padding的window_size, word_dim 50, 1) for news
                embedded_words_window_nopadding = embedded_words[:, first:last, :, :]

                paddings = [[0, 0], [0, 2 * args.d + 1 - (last - first)], [0, 0], [0, 0]]
                # (batch_size * max_click_history, 已padding的window_size(2*d+1), word_dim, 1) for users
                # (batch_size 128, 已padding的window_size, word_dim 50, 1) for news
                embedded_words_window = tf.pad(embedded_words_window_nopadding, paddings)
                windows.append(embedded_words_window)

            # (batch_size * max_click_history, 窗口数* 已padding的window_size(2*d+1), word_dim, 1) for users
            # (batch_size , 窗口数* 已padding的window_size, word_dim 50, 1) for news
            all_windows = tf.concat(windows, axis=1)

            # (batch_size * max_click_history * 窗口数, 已padding的window_size(2*d+1), word_dim, 1) for users
            # (batch_size * 窗口数, 已padding的window_size, word_dim 50, 1) for news
            all_windows = tf.reshape(all_windows, [-1, 2 * args.d + 1, args.word_dim, 1])

            # CNN
            outputs = []
            for filter_size in args.filter_sizes:
                filter_shape = [filter_size, args.word_dim, 1, args.n_filters]  # 每个卷积核的形状 [2或3,50,1,128]
                w = tf.get_variable(name='w_' + str(filter_size), shape=filter_shape, dtype=tf.float32)  # weight
                b = tf.get_variable(name='b_' + str(filter_size), shape=[args.n_filters], dtype=tf.float32)  # bias
                if w not in self.params:
                    self.params.append(w)
                """
                (batch_size * max_click_history 30, window_size - filter_size + 1 (2d+1 - 2 + 1或2d+1 - 3 + 1), 1, n_filters_for_each_size) for users
                (batch_size 128, window_size - filter_size + 1 (2d+1 - 2 + 1或2d+1 - 3 + 1), 1, n_filters_for_each_size 128) for news
                """
                # 卷积
                # strides： 卷积时在图像每一维的步长，这是一个一维的向量，[ 1, strides, strides, 1]，第一位和最后一位固定必须是1，中间两个数分别代表了水平滑动和垂直滑动步长值。
                # padding： string类型，值为“SAME” 和 “VALID”，表示的是卷积的形式，是否考虑边界。"SAME"是考虑边界，不足的时候用0去填充周围，"VALID"则不考虑。
                conv = tf.nn.conv2d(all_windows, w, strides=[1, 1, 1, 1], padding='VALID', name='conv')
                # 激活函数
                relu = tf.nn.relu(tf.nn.bias_add(conv, b), name='relu')

                # (batch_size * max_click_history* 窗口数, 1, 1, n_filters_for_each_size) for users
                # (batch_size* 窗口数 , 1, 1, n_filters_for_each_size ) for news
                # 最大池化
                pool = tf.nn.max_pool(relu, ksize=[1, (2 * args.d + 1) - filter_size + 1, 1, 1],
                                      strides=[1, 1, 1, 1], padding='VALID', name='pool')
                outputs.append(pool)

            # (batch_size * max_click_history* 窗口数, 1, 1, n_filters_for_each_size * n_filter_sizes) for users
            # (batch_size * 窗口数, 1, 1, n_filters_for_each_size * n_filter_sizes 16*3) for news
            output = tf.concat(outputs, axis=-1)

            # (batch_size * max_click_history * 窗口数, n_filters_for_each_size * n_filter_sizes) for users
            # (batch_size * 窗口数, n_filters_for_each_size * n_filter_sizes 16*3 ) for news
            output = tf.reshape(output, [-1, args.n_filters * len(args.filter_sizes)])
            #output = tf.nn.dropout(output, keep_prob=args.keep_prob)

            # (batch_size * max_click_history , 窗口数, n_filters_for_each_size * n_filter_sizes) for users
            # (batch_size , 窗口数, n_filters_for_each_size * n_filter_sizes 16*3 ) for news
            output_reshape = tf.reshape(output, [-1, args.n_windows, args.n_filters * len(args.filter_sizes)])


        with tf.name_scope("SelfAttention"):
            # shape(W_s1) = (n_filters_for_each_size * n_filter_sizes, d_a)
            W_s1 = tf.get_variable("W_s1", shape=[args.n_filters * len(args.filter_sizes), args.d_a_size])
            # shape(W_s2) = (d_a, r)
            W_s2 = tf.get_variable("W_s2", shape=[args.d_a_size, args.r_size])
            if W_s1 not in self.params:
                self.params.append(W_s1)
            if W_s2 not in self.params:
                self.params.append(W_s2)

            # (batch_size * max_click_history * 窗口数, r) for users
            # (batch_size * 窗口数, r) for news
            h2 = tf.matmul(tf.nn.tanh(tf.matmul(output, W_s1)), W_s2)

            # (batch_size * max_click_history, r, 窗口数) for users
            # (batch_size, r, 窗口数) for news
            h2_reshape = tf.transpose(tf.reshape(h2, [-1, args.n_windows, args.r_size]), [0, 2, 1])

            # (batch_size * max_click_history, r, 窗口数) for users
            # (batch_size, r, 窗口数) for news
            self.A = tf.nn.softmax(h2_reshape, name="attn")

        with tf.name_scope("SentenceEmbedding"):
            # (batch_size * max_click_history, r, n_filters_for_each_size * n_filter_sizes) for users
            # (batch_size, r, n_filters_for_each_size * n_filter_sizes) for news
            M = tf.matmul(self.A, output_reshape)

            # (batch_size * max_click_history, r * n_filters_for_each_size * n_filter_sizes) for users
            # (batch_size, r * n_filters_for_each_size * n_filter_sizes) for news
            M_flat = tf.reshape(M, shape=[-1, args.r_size * args.n_filters * len(args.filter_sizes)])
        return M_flat

    def _build_train(self, args):
        with tf.name_scope('train'):  # 增加命名空间，便于在tensorboard中展示清晰的逻辑关系图，不会对对象的作用域产生影响。
            # sigmoid交叉熵损失之后取均值
            self.base_loss = tf.reduce_mean(
                tf.nn.sigmoid_cross_entropy_with_logits(labels=self.labels,
                                                        logits=self.scores_unnormalized))  # logits:未归一化的概率
            # l2正则惩罚项
            self.l2_loss = tf.Variable(tf.constant(0., dtype=tf.float32), trainable=False)
            for param in self.params:
                self.param = param
                self.l2_loss = tf.add(self.l2_loss, args.l2_weight * tf.nn.l2_loss(self.param))
            # P惩罚项
            self.AA_T = tf.matmul(self.A, tf.transpose(self.A, perm=[0, 2, 1]))
            self.eye = tf.reshape(tf.tile(tf.eye(args.r_size), [tf.shape(self.A)[0], 1]),
                                  [-1, args.r_size, args.r_size])
            # compute Frobenius norm
            self.P = tf.square(tf.norm(self.AA_T - self.eye, axis=[-2, -1], ord='fro'))
            self.P_loss = tf.reduce_mean(self.P * args.p_coef)

            # 构造损失函数
            self.loss = self.base_loss + self.l2_loss + self.P_loss
            self.loss = self.base_loss + self.l2_loss
            print(self.loss)
            # 优化损失
            self.optimizer = tf.train.AdamOptimizer(args.lr).minimize(self.loss)

    # 每次训练
    def train(self, sess, feed_dict):
        return sess.run([self.loss, self.optimizer], feed_dict)  # feed_dict：传入值

    def eval(self, sess, feed_dict):
        labels, scores = sess.run([self.labels, self.scores], feed_dict)
        auc = roc_auc_score(y_true=labels, y_score=scores)
        f1 = f1_score(y_true=labels, y_pred=scores.round())
        return auc, f1
