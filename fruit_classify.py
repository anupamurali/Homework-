"""
Classifying fruits into 3 different classes

Use gradient ascent on the log likelihood
Anupa Murali
February 27, 2015
"""
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal 

csv_filename = 'fruit.csv'

fruit = []
width = []
height = []
with open(csv_filename, 'rU') as csv_fh:

    # Parse as a CSV file.
    reader = csv.reader(csv_fh, dialect='excel')

    # Skip the header line.
    next(reader, None)

    # Loop over the file.
    for row in reader:
        # Store the data.
        fruit.append(float(row[0]))
        width.append(float(row[1]))
        height.append(float(row[2]))

# Turn the data into numpy arrays.
fruit  = np.array(fruit)
N = len(fruit)
fruit_classifications = np.zeros((N,3))
for i in xrange(N):
    if fruit[i] == 1:
        fruit_classifications[i] = np.array([1,0,0])
    elif fruit[i] == 2:
        fruit_classifications[i] = np.array([0,1,0])
    elif fruit[i] == 3:
        fruit_classifications[i] = np.array([0,0,1])

width = np.array(width)
height = np.array(height)
X = np.vstack((width, height)).T

def denominator(X, w):
    S = 1 + sum([math.exp(np.dot(w[i], X.T)) for i in xrange(2)])
    return math.log(S)

def error_function(X, T, w):
    S = 0
    for n in xrange(N):
        for k in xrange(2):
            deno = float(Decimal(1.) + sum([Decimal(np.dot(w[i], 
                X[n].T)).exp() for i in xrange(2)]))
            S += T[n][k] * (np.dot(w[k], X[n].T) - deno)

    return -1*S

def softmax_params(X, T, w):
    Y = np.zeros((3, N))
    for n in xrange(N):
        for i in xrange(2):
            Y[i][n] = float(Decimal(np.dot(w[i], X[n].T)).exp()/ 
                (Decimal(1.) + sum([Decimal(np.dot(w[j], 
                    X[n].T)).exp() for j in xrange(2)])))

    return Y

def gradient_function(Y, T, X):
    S = np.zeros((2,2))
    for i in xrange(N):
        for k in xrange(2):
            S[k] += (Y[k][i] - T[i][k])*X[i]

    return S

maxIters = 200
epsilon = 0.001

def gradient_descent(X, T):
    w = np.ones((2, 2))
    Y = softmax_params(X, T, w)

    for i in xrange(maxIters):
        grad = gradient_function(Y, T, X)
        
        delta = np.linalg.norm(grad)
        if abs(delta) < epsilon:
            return w
        else:
            w += gradient_function(Y, T, X)
            Y = softmax_params(X, T, w)

    return w

w = gradient_descent(X, fruit_classifications)

Y = softmax_params(X, fruit_classifications, w)

def select_max_ind(vec):
    M = len(vec)
    maxi = 0
    max_ind = -1
    for i in xrange(M):
        if vec[i] > maxi:
            maxi = vec[i]
            max_ind = i

    return max_ind

Y_results = np.zeros(59)
for i in xrange(59):
    Y_results[i] = select_max_ind(Y[:,i])

print Y_results


    


    





