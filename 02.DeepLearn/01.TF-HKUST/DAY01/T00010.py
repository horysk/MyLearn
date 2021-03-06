# -*-coding:utf-8-*-
# @auth ivan
# @time 20180717
# @goal test the tf
import tensorflow as tf
import numpy as np
import random


print('\nM10')
# for reproducibility
tf.set_random_seed(777)
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('/data/project/Learn/TF/01.TF-HKUST/Data/', one_hot=True)
# http://yann.lecun.com/exdb/mnist/
print('Train: ', mnist.train.num_examples, 'Test: ', mnist.test.num_examples)
# parameters
nb_classes = 10
learning_rate = 0.001
training_epochs = 15
batch_size = 100
# MNIST data image of shape 28 * 28 = 784
X = tf.placeholder(tf.float32, [None, 784])
# 0 - 9 digits recognition = 10 classes
Y = tf.placeholder(tf.float32, [None, nb_classes])
W = tf.Variable(tf.random_normal([784, nb_classes]))
b = tf.Variable(tf.random_normal([nb_classes]))
# Hypothesis (using softmax)
hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
# Test model
is_correct = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
# Calculate accuracy
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

with tf.Session() as sess:
    # Initialize TensorFlow variables
    sess.run(tf.global_variables_initializer())
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples/batch_size)
        # 550 = 55000 / 100

        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            c, _ = sess.run(
                [cost, optimizer],
                feed_dict={X: batch_xs, Y: batch_ys}
            )
            # ~ WARNING: When c isnan then np.nan+1=np.nan.
            if np.isnan(c):
                c = 0
            avg_cost += c/total_batch

        print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))
    print("Learning finished")
    # Test the model using tPatterns sets
    print(
        "Accuracy: ",
        accuracy.eval(
            session=sess,
            feed_dict={X: mnist.test.images, Y: mnist.test.labels}
        )
    )
    # Get one and predict
    r = random.randint(0, mnist.test.num_examples - 1)
    print('Choose: %d' % r)
    print(
        "Label: ",
        sess.run(tf.argmax(mnist.test.labels[r:r + 1], 1))
    )
    print(
        "Prediction: ",
        sess.run(
            tf.argmax(hypothesis, 1),
            feed_dict={X: mnist.test.images[r:r + 1]}
        )
    )



