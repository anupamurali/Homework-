from __future__ import division
import pyopencl as cl

import numpy as np 
from coalesced_sum import coalesced
from blocked_sum import blocked

# We use either blocked or coalesced
# Run with is_blocked = True to run from blocked_sum

is_blocked = False
best_T = float("inf")
best_params = (1,16)
N = 10000000
hx = np.random.uniform(0, 1, N).astype(np.float32)
for i in xrange(8):
	for j in xrange(4,17):
		W = 2**i
		Ng = 2**j
		if is_blocked:
		    T = blocked(N, W, Ng, hx)[1]
		    print "THIS IS T = ",T
		else:
			T = coalesced(N, W, Ng, hx)[1]
        if T < best_T:
            best_T = T
            best_params = (W, Ng)
print "NUMPY RESULT = ",np.sum(hx)
print "BEST PARAMS = ",best_params
print "BEST TIME = ", best_T



