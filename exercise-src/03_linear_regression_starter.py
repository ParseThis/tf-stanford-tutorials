"""
Simple linear regression example in TensorFlow
This program tries to predict the number of thefts from 
the number of fire in the city of Chicago
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import xlrd
import pdb



DATA_FILE = '../data/fire_theft.xls'

def huber_loss(labels, predictions, delta=0.1):
    # tf.select deprecated in tf 1.0.1
    # https://github.com/tensorflow/tensorflow/issues/8647
    residuals = tf.abs(predictions - labels)
    
    # element wise comparison 
    condition = tf.less(residuals, delta)
    small_res = tf.square(residuals)
    large_res = delta * residuals - 0.5 * tf.square(delta)
    return tf.where(condition, small_res, large_res)
        
# Phase 1: Assemble the graph
# Step 1: read in data from the .xls file
book = xlrd.open_workbook(DATA_FILE, encoding_override='utf-8')
sheet = book.sheet_by_index(0)
data = np.asarray([sheet.row_values(i) for i in range(1, sheet.nrows)])
n_samples = sheet.nrows - 1

X_train = data[:, :-1]
Y_train = data[:, -1]
dims = X_train.shape[1]

# Step 2: create placeholders for input X (number of fire) and label Y (number of theft)

X = tf.placeholder(dtype=tf.float32, name="inputs")
Y = tf.placeholder(dtype=tf.float32, name="labels")

# Step 3: create weight and bias, initialized to 0
# name your variables w and b
W = tf.Variable(np.random.randn(), name="weights")
b = tf.Variable(np.random.randn(), name="bias")


# Step 4: predict Y (number of theft) from the number of fire
# name your variable Y_predicted

_y = tf.add(tf.multiply(X, W), b)
# Step 5: use the square error as the loss function
# name your variable loss

# loss = tf.reduce_sum(tf.pow(_y-Y, 2))/ (2 * n_samples)
# Step 6: using gradient descent with learning rate of 0.01 to minimize loss
# loss = tf.square(_y - Y, name="loss")
h_loss = huber_loss(Y, _y)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(h_loss)

init = tf.global_variables_initializer()
# Phase 2: Train our model
with tf.Session() as sess:
	# Step 7: initialize the necessary variables, in this case, w and b
	# TO - DO	
        sess.run(init)
	# Step 8: train the model
	for i in range(1000): # run 100 epochs
		total_loss = 0
                for x, y in zip(X_train, Y_train):
			# Session runs optimizer to minimixze loss and fetch the value of loss   
                        _, l = sess.run([optimizer, h_loss],  feed_dict = {X: x[0], Y: y})
                        total_loss+=l
		print "Epoch {0}: {1}".format(i, total_loss/n_samples)

        w, b = [W.eval(), b.eval()]
	
# plot the results

print("Plotting Model against data")
X, Y = data.T[0], data.T[1]

plt.plot(X, Y, 'bo', label='Real data')
plt.plot(X, X * w + b, 'r', label='Predicted data')
plt.legend()
plt.show()
