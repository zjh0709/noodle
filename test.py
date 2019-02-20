import tensorflow as tf
import numpy as np
import os


# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def read_data():
    return [("600597", "20170101", 4),
            ("000002", "20170101", 3),
            ("600104", "20170101", -1),
            ("600597", "20170102", 3),
            ("000002", "20170102", 3),
            ("600104", "20170102", -2),
            ("600597", "20170103", -5),
            ("000002", "20170103", -4),
            ("600104", "20170103", 2)]


# noinspection PyArgumentList
def trans_data(data):
    x, y, value_data = zip(*data)
    item_mapper = {k: idx for idx, k in enumerate(set(x))}
    date_mapper = {k: idx for idx, k in enumerate(set(y))}
    item_data = [item_mapper[d] for d in x]
    date_data = [date_mapper[d] for d in y]
    return item_data, date_data, value_data, item_mapper, date_mapper


def train(batch_size, item_embedding_size, date_embedding_size, item_size, date_size):
    graph = tf.Graph()
    with graph.as_default():
        with tf.name_scope('inputs'):
            train_item_inputs = tf.placeholder(tf.int32, shape=[batch_size, 1])
            train_date_inputs = tf.placeholder(tf.int32, shape=[batch_size, 1])
            train_values = tf.placeholder(tf.float32, shape=[batch_size, 1])
            # valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

        with tf.device("CPU:0"):
            with tf.name_scope('embeddings'):
                item_embeddings = tf.Variable(
                    tf.random_uniform([item_size, item_embedding_size], -1.0, 1.0, seed=42))
                item_embed = tf.nn.embedding_lookup(item_embeddings, train_item_inputs)

                date_embeddings = tf.Variable(
                    tf.random_uniform([date_size, date_embedding_size], -1.0, 1.0, seed=42))
                date_embed = tf.nn.embedding_lookup(date_embeddings, train_date_inputs)

                mat = tf.matmul(tf.transpose(item_embed, perm=[0, 2, 1]), date_embed)
                flat = tf.reshape(mat, shape=[batch_size, -1])

            with tf.name_scope('weights'):
                weights = tf.Variable(
                    tf.truncated_normal([item_embedding_size * date_embedding_size],
                                        stddev=1.0 / np.math.sqrt(item_size), seed=42))
                weights_exp = tf.tile(tf.expand_dims(weights, 0), [batch_size, 1])

            with tf.name_scope('biases'):
                biases = tf.Variable(tf.zeros([item_embedding_size * date_embedding_size]))
                biases_exp = tf.tile(tf.expand_dims(biases, 0), [batch_size, 1])

            with tf.name_scope("y"):
                y = 20 * (-0.5 + tf.nn.sigmoid(
                    tf.reduce_sum(tf.add(tf.multiply(weights_exp, flat), biases_exp), axis=1)))

            with tf.name_scope('loss'):
                loss = tf.nn.l2_loss(tf.subtract(x=y, y=train_values))

        optimizer = tf.train.AdamOptimizer(1.0).minimize(loss)

        # with tf.name_scope('weights'):
        #     weights = tf.Variable(
        #         tf.truncated_normal([item_size, 1],
        #                             stddev=1.0 / np.math.sqrt(item_size)))
        #     weights_exp = tf.tile(tf.expand_dims(weights, 0), [batch_size, 1, 1])
        #
        # with tf.name_scope('biases'):
        #     biases = tf.Variable(tf.zeros([2, 1]))
        #     biases_exp = tf.tile(tf.expand_dims(biases, 0), [batch_size, 1, 1])
        #
        # with tf.name_scope("y"):
        #     w = tf.add(tf.matmul(embed, weights_exp), biases_exp)
        #     y = tf.reduce_sum(w, axis=1)
        #
        # with tf.name_scope('loss'):
        #     loss = tf.nn.l2_loss(tf.subtract(x=y, y=train_labels))
        #
        # optimizer = tf.train.AdamOptimizer(1.0).minimize(loss)

        init = tf.global_variables_initializer()

    sess = tf.Session(graph=graph, config=tf.ConfigProto(device_count={'gpu': 0}))
    sess.run(init)
    for i in range(1000):
        _, loss_val = sess.run([optimizer, loss],
                               feed_dict={
                                   train_item_inputs: [[0], [1], [0], [1]],
                                   train_date_inputs: [[0], [0], [1], [1]],
                                   train_values: [[0.1], [0.2], [0.3], [0.4]]
                               })
        print(loss_val)

    # for i in range(10):
    #     _, loss_val = sess.run([optimizer, loss],
    #                            feed_dict={train_inputs: [[0, 1], [1, 0], [0, 0]],
    #                                       train_labels: [[0.1], [0.2], [0.3]]})
    #     print(loss_val)
    sess.close()


def main(_):
    data = read_data()
    item_data, date_data, value_data, item_mapper, date_mapper = trans_data(data)
    item_size, date_size = len(item_data), len(date_data)
    item_embedding_size = 5
    date_embedding_size = 6
    batch_size = 4
    train(batch_size, item_embedding_size, date_embedding_size, item_size, date_size)
    # with tf.Session() as sess:
    # embeddings = tf.Variable(name="embeddings",
    #                          initial_value=tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
    # embed = tf.nn.embedding_lookup(embeddings, [[0, 1], [1, 0], [0, 0]])
    # weights = tf.Variable(
    #     tf.truncated_normal([batch_size, embedding_size, 1],
    #                         stddev=1.0 / np.math.sqrt(embedding_size)))
    # biases = tf.Variable(tf.zeros([batch_size, 2, 1]))
    # init = tf.global_variables_initializer()
    # sess.run(init)
    # w = tf.add(tf.matmul(embed, weights), biases)
    # y = tf.reduce_sum(w, axis=1)
    # print(sess.run(w))
    # print(sess.run(y))


if __name__ == '__main__':
    tf.app.run()
