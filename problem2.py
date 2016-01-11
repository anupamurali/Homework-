import csv
import numpy as np
import pylab as pl
import random
import matplotlib.pyplot as plt
from scipy.stats import chi
from numpy import append, array, int8, uint8, zeros

def closest_distance(X, u, n, K):
	D = 100000
	best_k = -1
	for k in xrange(K):
	    if np.linalg.norm(X[n] - u[k]) <= D:
			D = np.linalg.norm(X[n] - u[k])


def kmeanspp(X, N, K):
    R = np.zeros((N,K))
    u = np.zeros((X[0].shape,K))
    k_init = random.randint(0, K-1) 
    Num = np.zeros(K)
    u[:,0] = X[k_init]
    Num[0] += 1
    D = np.zeros(N)
    P = np.zeros(N)
    for k in xrange(1,K):
    	for n in xrange(N):
            D[n] = closest_distance(X, u, n, k)
        
        D_norm = float(np.linalg.norm(D))**2
        for n in xrange(N):
        	P[n] = float(D[n])**2/D_norm

        xk = np.arange(N)
        n_rand = scipy.stats.rv_discrete(values=(xk,tuple(P)).rvs(size=1))
        new_S = u[k]*Num[k] + X[n_rand]
        Num[k] += 1
        u[k] = new_S/Num[k]





