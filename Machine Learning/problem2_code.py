import numpy as np 
import time
import matplotlib.pyplot as plt 

X = np.loadtxt('ratings.dat')

N = 100000

I_mask = np.ones(X.shape[0], dtype=bool)
I_test = np.random.choice(X.shape[0], N, replace=False)

num_users = int(np.unique(X[:,0]).max())
num_jokes = int(np.unique(X[:,1]).max())

train = X[:N]
X_train = np.zeros([num_users, num_jokes])

for user, joke_num, r in train:
    X_train[user-1][joke_num-1] = r

test = X[N:2*N]
X_test = np.zeros([num_users, num_jokes])
for user, joke_num, r in test:
    X_test[user-1][joke_num-1] = r

std_dv = 5.0
sigma = 1.0
K = 2

def get_mses(X_train, X_test, preds):
    valid_indices = X_train > 0
    train_mses = (X_train[valid_indices] - preds[valid_indices])**2
    train_mse = np.sqrt(np.sum(train_mses) / float(train_mses.size))

    valid_indices = X_test > 0
    test_mses = (X_test[valid_indices] - preds[valid_indices])**2
    test_mse = np.sqrt(np.sum(test_mses) / float(test_mses.size))

    return train_mse, test_mse

def get_loglikelihoods(X_train, X_test, preds, sigma):
    valid_indices = X_train > 0
    ll = -1.0/(2 * sigma * sigma) * (X_train[valid_indices] - preds[valid_indices])**2
    ll += -np.log(sigma) - 0.5 * np.log(2.0 * np.pi)
    train_ll = np.sum(ll)
    
    valid_indices = X_test > 0
    ll = -1.0/(2 * sigma * sigma) * (X_test[valid_indices] - preds[valid_indices])**2
    ll += -np.log(sigma) - 0.5 * np.log(2.0 * np.pi)
    test_ll = np.sum(ll)
    
    return train_ll, test_ll
    
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
    train_lls = []
    test_lls= []
    for k in range(100):
        # Update parameters for U
        sigma_u_new = np.linalg.inv(np.linalg.inv(sigma_u) + V.T.dot(V))
        mu_u_new = sigma_u_new.dot(V.T.dot(X_train.T) + np.linalg.inv(sigma_u).dot(mu_u.T)).T
        sigma_u = sigma_u_new
        mu_u = mu_u_new

        # Update parameters for V
        sigma_v_new = np.linalg.inv(np.linalg.inv(sigma_v) + U.T.dot(U))
        mu_v_new = sigma_v_new.dot(U.T.dot(X_train) + np.linalg.inv(sigma_v).dot(mu_v.T))
        sigma_v = sigma_v_new
        mu_v = mu_v_new.T

         # Update U values
        for i in range(num_users):
            U[i] = np.random.multivariate_normal(mu_u[i], sigma_u)
         
        # Update V values
        for j in range(num_jokes):
            V[j] = np.random.multivariate_normal(mu_v_new[:,j],sigma_v)

        # Get predictions for R
        preds = U.dot(V.T)
        trainmse, testmse = get_mses(X_train, X_test, preds)
        trainll, testll = get_loglikelihoods(X_train, X_test, preds, 1.0)
        train_mses.append(trainmse)
        test_mses.append(testmse)        
        train_lls.append(trainll)
        test_lls.append(testll)

    return train_mses, test_mses, train_lls, test_lls
	
all_train_mses = []
all_test_mses = []
all_train_lls = []
all_test_lls = []

for k_val in xrange(1,11):
    print "=== USING K={0} ===".format(k_val)
    train_mses, test_mses, train_lls, test_lls = gibbs(k_val, X_train, X_test)
    all_train_mses.append(train_mses[-1])
    all_test_mses.append(test_mses[-1])
    all_train_lls.append(train_lls[-1])
    all_test_lls.append(test_lls[-1])
    plot_types = [("Train MSE K={0}", "trainmses", train_mses),
                  ("Test MSE K={0}", "testmses", test_mses),
                  ("Train Log Likelihood K={0}", "trainloglikelihood", train_lls),
                  ("Test Log Likelihood K={0}", "testloglikelihood", test_lls)]
    for title, fname, data in plot_types: 
        plt.figure()
        plt.plot(data)
        plt.title(title.format(k_val))
        plt.savefig("Plots/K{0}{1}.png".format(k_val, fname))

plot_types = [("Train MSE vs. K", "trainmsesvsk", all_train_mses),
              ("Test MSE vs. K", "testmsesvsk", all_test_mses),
              ("Train Log Likelihood vs. K", "trainloglikelihoodvsk", all_train_lls),
              ("Test Log Likelihood vs. K", "testloglikelihoodvsk", all_test_lls)]

for title, fname, data in plot_types: 
    plt.figure()
    plt.plot(data)
    plt.title(title)
    plt.savefig("Plots/{0}.png".format(fname))