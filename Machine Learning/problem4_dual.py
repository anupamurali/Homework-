import csv
import numpy as np
import pylab as pl
from cvxopt import matrix
from cvxopt import solvers
import matplotlib.pyplot as plt


csv_filename = 'fruit.csv'

fruit  = []
width = []
height = []
with open(csv_filename, 'rU') as csv_fh:

    # Parse as a CSV file.
    reader = csv.reader(csv_fh, dialect='excel')

    # Skip the header line.
    next(reader, None)

    # Loop over the file.
    for row in reader:

        # Store the data. Only store if either apple or lemon.
        if not (int(row[0]) == 2):
            fruit.append(float(row[0]))
            width.append(float(row[1]))
            height.append(float(row[2]))

# Turn the data into numpy arrays.
print fruit
fruit  = np.array(fruit)
N = len(fruit)
T = np.zeros(N)
for i in xrange(N):
    # apple
    if fruit[i] == 1:
        T[i] = 1
    # lemon
    elif fruit[i] == 3:
        T[i] = -1

width = np.array(width)
height = np.array(height)
X = np.vstack((width, height,np.ones(N))).T
X_old = np.vstack((width, height)).T
"""
The following is an implementation of the dual problem
"""

P = np.zeros((N,N))
for i in xrange(N):
    for j in xrange(N):
        P[i][j] = T[i]*T[j]*np.dot(X_old[i].T,X_old[j])

print P
#print "T shape = ",T.shape
#print "X shape = ",X.shape

G = np.identity(N)

h = np.zeros(N)
#print G

A = np.matrix(T)
b = 0
q = -np.ones(N)

P = matrix(P, tc='d')
q = matrix(q, tc='d')
G = matrix(G, tc='d')
h = matrix(h, tc='d')
A = matrix(A, tc='d')
b = matrix(b, tc='d')

# initialize a solver
sol = solvers.qp(P,q,-G,-h,A,b)
# The following is our desired w, b
print sol['x']
print sol['dual objective'] 

a = np.array(sol['x'])
for i in xrange(N):
    if a[i] > 0.001:
        print "alpha = ",a[i]
        print "index = ",i
        print "width = ",width[i]
        print "height = ",height[i]
        print "fruit = ",fruit[i]












