import numpy as np
from scipy.linalg import sqrtm 
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import math
data = np.loadtxt('CASP.csv', delimiter = ',', skiprows = 1)

y = data[:, 0]
X = data[:, 1 : ]


def split_train_test(X, y, fraction_train = 9.0 / 10.0): 
	end_train = round(X.shape[ 0 ] * fraction_train) 
	X_train = X[ 0 : end_train, ] 
	y_train = y[ 0 : end_train ] 
	X_test = X[ end_train :, ] 
	y_test = y[ end_train : ] 
	return X_train, y_train, X_test, y_test


def normalize_features(X_train, X_test): 
	mean_X_train = np.mean(X_train, 0) 
	std_X_train = np.std(X_train, 0) 
	std_X_train[ std_X_train == 0 ] = 1 
	X_train_normalized = (X_train - mean_X_train) / std_X_train 
	X_test_normalized = (X_test - mean_X_train) / std_X_train 
	return X_train_normalized, X_test_normalized

def rmse(y, y_pred):
	return mean_squared_error(y, y_pred)**0.5

def rmse_alternative(y, y_pred):
	n = y.shape[0]
	error = 0
	for i in range(n):
		error += (y[i] - y_pred[i])**2

	error = error/n
	return error**0.5



X_train, y_train, X_test, y_test = split_train_test(X, y)
X_train, X_test = normalize_features(X_train, X_test)
X_train = np.concatenate((X_train, np.ones((X_train.shape[ 0 ], 1))), 1)
X_test = np.concatenate((X_test, np.ones((X_test.shape[ 0 ], 1))), 1)


"""
Problem 4: MAP using QR Decomposition
"""
D = X_train[0].size
Gamma = np.identity(D)*10
Gamma_sqrt = np.linalg.cholesky(Gamma)
X_tilde = np.vstack((X_train, Gamma_sqrt))
y_tilde = np.hstack((y_train, np.zeros(10)))

Q, R = np.linalg.qr(X_tilde)
w_hat = np.dot(np.dot(np.linalg.inv(R),Q.T), y_tilde)

print "WEIGHTS = ", w_hat
y_test_result = np.dot(X_test, w_hat)

errors = y_test - np.dot(X_test, w_hat)
rmse = math.sqrt(sum(errors**2))

"""
Problem 5: L-BFGS
"""

def obj_and_gradient(X, y):
    def log_posterior(w) :
        return 0.5 * np.sum((y - X.dot(w))**2) - 5*(w.dot(w))
    
    def grad(w) :
        return w.T.dot(X.T.dot(X)) + 10 * w - X.T.dot(y)
        
    return (log_posterior, grad)

(obj, grad) = obj_and_gradient(X_train, y_train)

w0 = np.zeros(10)
w_problem5 = minimize(fun=obj, x0=w0, method='L-BFGS-B', jac=grad, options={'maxiter':100}).x
print "PROBLEM 5 WEIGHTS = ", w_problem5
y_pred = np.dot(X_test, w_problem5)
rmse = rmse_alternative(y_test, y_pred)
print "PROBLEM 5 RMSE = ",rmse



print "=============="
print "START PROBLEM 6"
print "=============="

# QR Code for 6
import math
import time


def design_matrix(X, A):
    lst_arr = []
    for i in range(X.shape[0]) :
        lst_arr.append(np.cos(A.dot(X[i, :])))

    return np.array(lst_arr)
D = [100, 200, 400, 600]

data = np.loadtxt('CASP.csv', delimiter=',', skiprows=1)

# creating capital A
QR_time = []
QR_RMSE = []
for d in D :
    lst_rows = []
    for i in range(d):
        a = np.random.multivariate_normal(mean=np.zeros(9), cov=np.identity(9))
        b = np.random.uniform(low=0.0, high=2 * np.pi)

        row = np.append(a, b)
        lst_rows.append(row)

    A = np.array(lst_rows)

    X_train_curr = design_matrix(X_train, A)
    X_test_curr = design_matrix(X_test, A)

    # pad matrices X and vector Y for ridge regression
    for i in range(d):
        row = np.zeros((1, X_train_new.shape[1]))
        row.itemset((0, i), 10)
        np.hstack((X_train_new, row), axis=0)
        np.concatenate((X_train_curr, row), axis=0)
        np.concatenate((y_train, np.zeros((1,))), axis=0)
        np.concatenate((y_test, np.zeros((1,))), axis=0)

    time_start = time.time()

    Q_train, R_train = np.linalg.qr(X_train_new)
    Q_test, R_test = np.linalg.qr(X_test_new)

    z_train = Q_train.T.dot(y_train)
    z_test = Q_test.T.dot(y_test)

    # solve R w = z
    w_MAP = np.linalg.solve(R_train, z_train)

    running_time = time.time() - time_start

    QR_time.append(running_time)

    target_estimate = X_test_curr.dot(w_MAP)

    QR_RMSE.append(math.sqrt(np.sum(np.square(target_estimate - y_test)) / y_test.shape[0]))

print "QR TIME =",QR_time
print "QR RMSE = ",QR_RMSE


# In[ ]:

# L_BFGS Code for 6
import math
import time

def design_matrix(X, A):
    lst_arr = []
    for i in range(X.shape[0]) :
        lst_arr.append(np.cos(A.dot(X[i, :])))

    return np.array(lst_arr)
D = [100, 200, 400, 600]

data = np.loadtxt('CASP.csv', delimiter=',', skiprows=1)

BFGS_time = []
BFGS_RMSE = []

# creating capital A
for d in D :
    lst_rows = []
    for i in range(d):
        a = np.random.multivariate_normal(mean=np.zeros(9), cov=np.identity(9))
        b = np.random.uniform(low=0.0, high=2 * np.pi)

        row = np.append(a, b)
        lst_rows.append(row)

    A = np.array(lst_rows)

    X_train_curr = design_matrix(X_train, A)
    X_test_curr = design_matrix(X_test, A)

    time_start = time.time()

    (obj, grad) = obj_and_gradient(X_train_curr, y_train)
    w_estimate = minimize(fun=obj, x0=np.zeros(d), method='L-BFGS-B', jac=grad, options={'maxiter':100}).x
    
    running_time = time.time() - time_start

    predictions = X_test_curr.dot(w_estimate)
    RMSE = np.sqrt(np.mean((predictions-y_test)**2))
    
    BFGS_time.append(running_time)
    BFGS_RMSE.append(RMSE)

print "BFGS TIME = ",BFGS_time
print "BFGS RMSE = ",BFGS_RMSE



# In[26]:

# Plotting Code
from pylab import *

# xlabel('time')
# ylabel('RMSE')
# plot(QR_time, QR_RMSE, 
#         'ro', label='QR')

xlabel('time')
ylabel('RMSE')
plot(BFGS_time, BFGS_RMSE, 
        'ro', label='BFGS')

# Show the plot
legend()
savefig('P6.png')
show()


