import numpy as np
import heapq

N_VAL = 100
M_VAL = 100000
D = np.random.rand(N_VAL, M_VAL)
D_norm = np.zeros((N_VAL,M_VAL))

for i in xrange(M_VAL):
    D_norm[:,i] = D[:,i]/np.linalg.norm(D[:,i])
z_actual = np.random.rand(M_VAL,1)
x = np.dot(D,z_actual)
# print z_actual.shape

# print "DICTIONARY D = "
# print D
# print "X = "
# print x
# print "ACTUAL z = ",z_actual

# We're going to try to approximate z
def MP_serial(D, x):
    N, M = D.shape
    num_iter = 50
    z = np.zeros((M, 1))
    r = np.copy(x)
    z_temp = {}

    while np.linalg.norm(r) >= 0.3:
        # Maximize inner product between D and r
        z_temp = {}
        for i in xrange(M):
            z_temp[i] = np.dot(D[:,i],r)

        max_pos = max(z_temp.iterkeys(), key=lambda k: abs(z_temp[k]))

        z[max_pos] = np.dot(D[:,max_pos].T,r)
        r = r - (z[max_pos]*D[:,max_pos]).reshape((N,1))
        print "R NORM = ", np.linalg.norm(r)

    return z 

z = MP_serial(D_norm, x)
print z 
print z.shape

x_mp = np.dot(D, z)
# print 'ACTUAL X = ',x
# print "X FROM MP = ",x_mp
# print "Z=", z
# print "NORM D=", np.linalg.norm(D[:,4])

for i in xrange(N_VAL):
    print x[i][0], x_mp[i][0]

def MP_serial2(D, x):
    K = 10
    num_select = 10
    N, M = D.shape
    z = np.zeros((num_select,N))
    r = np.copy(x)
    x_temp = {}
    
    for k in xrange(K):
        # Maximize inner product between D and r
        for i in xrange(N):
            x_temp[i] = np.dot(D[i].T.reshape((M,1)),x.T)
        x_largest = heapq.nlargest(num_select, x_temp)
        for i in xrange(num_select):
            print z[i].shape
            print np.dot(D[i].reshape((5,1)),r.T).shape
            print r.T.shape
            print D[i].shape
            z[i] = np.dot(D[i].reshape((5,1)),r.T)
            
        # Compute residual
        for i in xrange(num_select):
            r = r - np.dot(D[i].reshape((5,1)), z[i].reshape((1,100))).T
    
    return z