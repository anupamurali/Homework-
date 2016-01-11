import numpy as np
import math
from scipy.optimize import minimize

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

def approx(obj, w, i):
    row = np.zeros(10)
    row.itemset(i, 1)

    return (obj(w + 0.1 * row) - obj(w - 0.1 * row)) / 0.2


def obj_and_gradient(X, y):
    def obj(w):
        return 0.5 * np.sum(np.square(y - X.dot(w))) + 5 * w.dot(w)

    def grad(w):
        return w.T.dot(X.T.dot(X)) + 10 * w - X.T.dot(y)

    return obj, grad


def normalize_features(X_train, X_test):
    mean_X_train = np.mean(X_train, 0)
    std_X_train = np.std(X_train, 0)
    std_X_train[ std_X_train == 0 ] = 1
    X_train_normalized = (X_train - mean_X_train) / std_X_train
    X_test_normalized = (X_test - mean_X_train) / std_X_train
    return X_train_normalized, X_test_normalized


def split_train_test(X, y, fraction_train = 9.0 / 10.0):
    end_train = round(X.shape[ 0 ] * fraction_train)
    X_train = X[ 0 : end_train, ]
    y_train = y[ 0 : end_train ]
    X_test = X[ end_train :, ]
    y_test = y[ end_train : ]
    return X_train, y_train, X_test, y_test


def main():
    # params
    sqrt_lambda = 10.0
    data = np.loadtxt('CASP.csv', delimiter=',', skiprows=1)

    y = data[:, 0]
    X = data[:, 1:]
    X_train, y_train, X_test, y_test = split_train_test(X, y)
    X_train, X_test = normalize_features(X_train, X_test)

    X_train = np.concatenate((X_train, np.ones((X_train.shape[0], 1))), 1)
    X_test = np.concatenate((X_test, np.ones((X_test.shape[0], 1))), 1)

    # verify the gradient computation is correct
    obj, grad = obj_and_gradient(X_train, y_train)
    w_tst = np.random.rand(10)
    for i in range(10):
        if (approx(obj, w_tst, i) - grad(w_tst)[i] < 1e-5):
            print str(i) + "th component of the gradient" + " matches the partial derivative wrt to W_" + str(i) +  " approximation"

    map_estimate_w = minimize(fun=obj, x0=np.zeros(10), method='L-BFGS-B', jac=grad, options={'maxiter': 100}).x

    print map_estimate_w

    target_estimate = X_test.dot(map_estimate_w)

    print math.sqrt(np.sum(np.square(target_estimate - y_test)) / y_test.shape[0])


if __name__ == "__main__":
    main()