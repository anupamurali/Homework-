import numpy as np

Z = np.array()
Z.append([7,1,11,11,7,11,3,1,2,21,1,11,10])
Z.append([26,29,56,31,52,55,71,31,54,47,40,66,68])
Z.append([6,15,8,8,6,9,17,22,18,4,23,9,8])
Z.append([60,52,20,47,33,22,6,44,22,26,34,12,12])

X = np.zeros((4,13))
for i in xrange(4):
    X[i] = row - np.mean(Z[1])

print X