import csv
import numpy as np
import pylab as pl
import math
import pandas as pd
import matplotlib.pyplot as plt
import math

"""
Use Ridge Regression to compute a best fit line for data
"""

fname = 'train_rad3_bit4096.csv'
fname2 = 'test.csv'

num_rows = 40000
data_offset = num_rows/2
df = pd.read_csv(fname,nrows=num_rows)
train_df = df.iloc[0:data_offset,:]
test_df = df.iloc[data_offset:num_rows,:]

X = np.array(train_df.drop('smiles', 1).drop('gap', 1))
Y = train_df['gap']
Y_test = test_df['gap']

X_test = np.array(test_df.drop('smiles', 1).drop('gap', 1))

alpha = 2

def ridge_regression(alpha):
	L = alpha*np.identity(4096)
	w = np.linalg.solve(np.dot(X.T, X) + np.dot(L.T, L) , np.dot(X.T, Y))
	results = np.dot(X_test, w)
	errors = np.zeros(data_offset)
	for i in xrange(data_offset):
		errors[i] = (results[i] - Y_test[i+data_offset])**2
	return alpha, math.sqrt(np.mean(errors)), w

def hillclimb():
	olderror = 10000
	thresh = 0.01
	step = 0.001
	error = 0
	alpha = 1
	while olderror - error > thresh:
		print "TESTING ALPHA = ",alpha
		upalpha, uperror, upw = ridge_regression(alpha+step)
		downalpha, downerror, downw = ridge_regression(alpha-step)
		if uperror < downerror:
			alpha = upalpha
			error = uperror
			w = upw
		else:
			alpha = downalpha
			erorr = downerror
			w = downw
		error = min(uperror, downerror)
	return alpha, w

alpha = 0.948
_, _, w = ridge_regression(alpha)
results = np.dot(X_test, w)

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score

errors = np.zeros(data_offset)
for i in xrange(data_offset):
	errors[i] = (results[i] - Y_test[i+data_offset])**2
print "RMSE = ", math.sqrt(np.mean(errors))
print "STD DEVIATION = ", np.std(errors)
print "ALPHA: ", alpha
    
plt.hist(errors)
plt.show()