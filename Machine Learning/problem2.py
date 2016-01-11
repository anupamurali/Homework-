import numpy as np 
import time
import matplotlib.pyplot as plt 


X = np.loadtxt('ratings.dat')

N = 100000

I_mask = np.ones(X.shape[0], dtype=bool)
I_test = np.random.choice(X.shape[0], N, replace=False)
I_mask[I_test] = 0

num_users = int(np.unique(X[:,0]).max())
num_jokes = int(np.unique(X[:,1]).max())

train = X[:100000]
X_train = np.zeros([num_users, num_jokes])

for user, joke_num, r in train:
    X_train[user-1][joke_num-1] = r

test = X[100000:200000]
X_test = np.zeros([num_users, num_jokes])
for user, joke_num, r in test:
    X_test[user-1][joke_num-1] = r

K = 2 
std_dv = 5.0
sigma = 1.0

def gibbs(K, X_train, X_test):
    ratings_predictions = np.zeros([num_users, num_jokes])
    U = np.zeros([num_users, K])
    V = np.zeros([num_jokes, K])
    sigma_u = std_dv * np.identity(K)
    mu_u = np.zeros((num_users, K))
    sigma_v = std_dv * np.identity(K)
    mu_v = np.zeros((num_jokes, K))
    train_mses = []
    test_mses = []
    for k in range(100):
        print "Step" + str(k)
        sigma_u_new = np.linalg.inv(np.linalg.inv(sigma_u) + V.T.dot(V))
        mu_u_new = sigma_u_new.dot(V.T.dot(X_train.T) + np.linalg.inv(sigma_u).dot(mu_u.T)).T
        sigma_u = sigma_u_new
        mu_u = mu_u_new
        for i in range(num_users):
            U[i] = np.random.multivariate_normal(mu_u[i], sigma_u)

        sigma_v_new = np.linalg.inv(np.linalg.inv(sigma_v) + U.T.dot(U))
        mu_v_new = sigma_v_new.dot(U.T.dot(X_train) + np.linalg.inv(sigma_v).dot(mu_v.T))
        sigma_v = sigma_v_new
        mu_v = mu_v_new.T
        for j in range(num_jokes):
            V[j] = np.random.multivariate_normal(mu_v_new[:,j],sigma_v)
        # Make predictions
        preds = U.dot(V.T)
        # Calculate train and test error
        valid_indices = X_train > 0
        mses = (X_train[valid_indices] - preds[valid_indices])**2
        mse = np.sqrt(np.sum(mses) / float(mses.size))
        train_mses.append(mse)
        print "TRAIN : " + str(mse)
        valid_indices = X_test > 0
        mses = (X_test[valid_indices] - preds[valid_indices])**2
        mse = np.sqrt(np.sum(mses) / float(mses.size))
        test_mses.append(mse)
        print "TEST : " + str(mse)
    return train_mses, test_mses

print gibbs(K, X_train, X_test)