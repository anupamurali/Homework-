import csv
import numpy as np
import pylab as pl
import math
import pandas as pd

fname = 'train.csv'

train_df = pd.read_csv(fname,nrows=20)

train_data = train_df.drop('smiles',1).drop('gap',1)
target_col = train_df['gap']

feat_list = [j for j in xrange(5)]
num_feats = len(feat_list)
small_train = train_data.iloc[:,feat_list]

X = small_train.as_matrix()
Y = target_col.as_matrix()

alpha = 0.01
L = alpha * np.identity(256)

w = np.linalg.solve(np.dot(X.T, X) + np.dot(L.T, L), np.dot(X.T, Y))
print w


