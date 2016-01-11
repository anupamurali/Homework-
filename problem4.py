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

"""
The following is an implementation of the primal problem
"""

q = np.zeros(3)
P = [[1,0,0],[0,1,0],[0,0,0]]
P = np.array(P)
#print "T shape = ",T.shape
#print "X shape = ",X.shape

G = np.zeros((N,3))

for i in xrange(N):
    G[i] = T[i]*X[i]

print G

h = np.ones(N)
#print G

P = matrix(P, tc='d')
q = matrix(q, tc='d')
G = matrix(G, tc='d')
h = matrix(h, tc='d')

A = 0
b = 0
# initialize a solver
sol = solvers.qp(P,q,-G,-h)
# The following is our desired w, b
print sol['x']
print sol['primal objective'] 

W = np.array(sol['x'])
print W

print np.dot(X,W).T

# We now plot the decision boundary 
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
print x_min, x_max
delta = 0.02
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, delta),
                     np.arange(y_min, y_max, delta))

# Put the result into a color plot
Z = np.zeros((xx.shape))
for i in xrange(xx.shape[0]):
    for j in xrange(xx.shape[1]):
        Z[i][j] = np.dot(np.array([xx[i][j],yy[i][j],1]),W)
        Z[i][j] = Z[i][j]/abs(Z[i][j])

plt.contourf(xx, yy, Z, cmap=pl.cm.Paired)
plt.axis('off')

# Plot also the training points
plt.scatter(X[:, 0], X[:, 1], c=T, cmap=pl.cm.Paired)

plt.show()













