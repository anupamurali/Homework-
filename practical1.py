import csv
import numpy as np
import pylab as pl
import math
import pandas as pd
import matplotlib as plt
import sklearn
import sklearn.decomposition
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score

NUM_DATA_POINTS = 10000
NUM_TEST_POINTS = 5000 #strictly less than NUM_DATA_POINTS

fname = 'train.csv'

train_df = pd.read_csv(fname,nrows=NUM_DATA_POINTS)

X_df = train_df.drop('smiles', 1).drop('gap', 1)
Y = train_df['gap']

X = X_df.as_matrix()

X_train = X[:NUM_TEST_POINTS]
X_test = X[NUM_TEST_POINTS:]
Y_train = Y[:NUM_TEST_POINTS]
Y_test = Y[NUM_TEST_POINTS:]

def test_prediction(Y_predict):
    deviations = Y_predict - Y_test
    return math.sqrt(np.dot(deviations, deviations) / len(deviations))

#######################################################
# SVD
#######################################################

svd = sklearn.decomposition.TruncatedSVD(n_components=20)
X_nd = svd.fit_transform(X_train)
#plt.scatter(x_2d[:,0], x_2d[:,1], c=Y, s = 50, cmap=plt.cm.Paired)
#plt.show()

lr_svd = sklearn.linear_model.LinearRegression()
lr_svd_model = lr_svd.fit(X_nd,Y_train)
Y_predict_lr_svd = lr_svd_model.predict(svd.fit_transform(X_test))
print 'svd: ', test_prediction(Y_predict_lr_svd)

#######################################################
# Linear model
#######################################################

import sklearn.linear_model

lr = sklearn.linear_model.LinearRegression()
lr_model = lr.fit(X_train,Y_train)

Y_predict_lr = lr_model.predict(X_test)
print 'linear regression: ', test_prediction(Y_predict_lr)



#######################################################
# Random Forest
#######################################################

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score


rfc = RandomForestClassifier(n_estimators=20)

print "RANDOM FOREST = ",rfc
scores = cross_val_score(rfc, X, Y.as_matrix())
print scores






















 