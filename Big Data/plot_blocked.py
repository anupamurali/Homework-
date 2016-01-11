from __future__ import division
import pyopencl as cl

#import matplotlib.pyplot as plt

import numpy as np 
from blocked_sum import blocked

best_T = float("inf")
best_params = (1,16)
bandwidths = []
#hx = np.random.uniform(0, 1, N).astype(np.float32)
for n in xrange(100,N+1):
    hx = np.random.uniform(0, 1, n).astype(np.float32)
    bandwidths.append((n, blocked(n, 64, 1024, hx)[0]))

print "ALL BANDWIDTHS = ",bandwidths