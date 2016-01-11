"""
Load data
"""
import graphlab
import numpy as np

train_file = open("/Users/Anupa/Dropbox/train-mnist-dense-with-labels.data", "r")
test_file = open("/Users/Anupa/Dropbox/test-mnist-dense-with-labels.data", "r")

train = np.loadtxt(train_file, delimiter=',')
train = np.delete(train, 1, axis=1)
print train.shape
test = np.loadtxt(test_file, delimiter=',')
print test.shape
test = np.delete(test, 1, axis=1)
print "got data"


# data = graphlab.SFrame(train)
# test_data = graphlab.SFrame(test)
# training_data, validation_data = data.random_split(0.8)

# """
# Serial Matching Pursuit. Solve for z in x = Dz.
# """
# def MP_serial(D, x):
#     N, M = D.shape
#     num_iter = 30
#     z = np.zeros((M, 1))
#     r = np.copy(x)
#     z_temp = {}

#     for itr in xrange(num_iter):
#         # Maximize inner product between D and r
#         z_temp = {}
#         for i in xrange(M):
#             z_temp[i] = np.dot(D[:,i],r)
#         max_pos = max(z_temp.iterkeys(), key=lambda k: abs(z_temp[k]))

#         z[max_pos] = np.dot(D[:,max_pos].T,r)
#         r = r - (z[max_pos]*D[:,max_pos])

#     return z 


# """
# Train a K-means dictionary on training set
# """
# def k_means(train_data, K):
#     kmeans = graphlab.kmeans.create(train_data, num_clusters=K)
#     return kmeans

# K = 10
# model = k_means(training_data, K)

# print model

# # Make dictionary out of K-means model
# #print model['cluster_info'][0]['X1']
# D = np.array([np.array(model['cluster_info'][i]['X1']) for i in range(K)])
# D = D.T
# print training_data.shape

# # Test serial MP implementation
# x = np.array([np.array(training_data[i]['X1']) for i in xrange(48000)])[0]
# #x = training_data
# u_x = np.array([np.mean(x[i]) for i in xrange(K)])
# # for i in xrange(K):
# #     x[i] = x[i]/255
# D_norm = np.zeros(D.shape)
# for i in xrange(K):
#     D_norm[:,i] = D[:,i]/np.linalg.norm(D[:,i])
      
# z = MP_serial(D_norm,x)

# print "X = "
# print x
# print "APPROX DOT PROD = "
# print np.dot(D,z)