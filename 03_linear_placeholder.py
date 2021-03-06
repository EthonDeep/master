import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
# import numpy as np
import matplotlib.pyplot as plt
import time
import utils

DATA_FILE = 'data/birth_life_2010.txt'

# Step 1: read in the data
data, n_samples = utils.read_birth_life_data(DATA_FILE)

# X, Y = iterator.get_next()
X = tf.placeholder(tf.float32, name="X")
Y = tf.placeholder(tf.float32, name="Y")

# Step 3: create weight and bias, initialized to 0
w = tf.get_variable('weight', initializer=tf.constant(0.0))
b = tf.get_variable('bias', initializer=tf.constant(0.0))

# Step 4: build model to predict Y
Y_predicted = w * X + b

# Step 5: use the square error as the loss function
loss = tf.square(Y - Y_predicted, name="loss")

# Step 6: using gradient descent with learning rate of 0.001 to minimize loss
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

starttime = time.time()

with tf.Session() as sess:
    # Step 7: initialize the necessary variables, in this case, w and b
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter('./graphs/linear_placeholder', sess.graph)
    # Step 8: train the model for 100 epochs
    for i in range(100):
        total_loss = 0
        for x, y in data:
            _, l = sess.run([optimizer, loss], feed_dict={X: x, Y: y})
            total_loss += l
        print('Epoch {0}: {1}'.format(i, total_loss / n_samples))
    writer.close()
    w_out, b_out = sess.run([w, b])
    print('w: %f, b: %f' % (w_out, b_out))

print('Took: %f seconds' % (time.time() - starttime))
# plot the results
plt.plot(data[:, 0], data[:, 1], 'bo', label='Real data')
plt.plot(data[:, 0], data[:, 0] * w_out + b_out, 'r', label='Predicted data with squared error')
# plt.plot(data[:,0], data[:,0] * (-5.883589) + 85.124306, 'g', label='Predicted data with Huber loss')
plt.legend()
plt.show()
