import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize
from sklearn import cross_validation

# Sigmoid functions
def log_sigmoid(a):
    if a < 0:
        return a-math.log(1 + math.e**a)
    else:
        return -1*math.log(1+math.e**(-a))


def sigmoid(a):
    if a < 0:
        return math.e**a/(1+math.e**a)
    else: 
        return 1/(1+math.e**(-a))

def basis_vec(x, D):
    vec = [1 if i == 0 else x**i for i in range(D)]
    return vec

def get_phi(x, D):
    return np.array([basis_vec(x[i], D) for i in range(10)])

def normalize(X_train, X_test):
    mu_train = np.mean(X_train, 0)
    pass

def approx_grad(objective, w, h) :
    grad = np.zeros(w.shape)
    for i in range(grad.size) :
        a = np.zeros(w.shape)
        a[i] = h
        grad[i] = (objective(w+a) - objective(w-a)) / (2 * h)
    return grad

# create objective, gradient, and hessian given 
# data 
def get_OGH(X, y, lambd):
    n = X.shape[0]
    m = X.shape[1]
    def objective(w):
        log_likelihood = 0
        for i in range(n):
            dat = X[i]
            function_est = w.T.dot(dat)
            if y[i] == 1:
                log_likelihood += log_sigmoid(function_est)
            else:
                log_likelihood += -1*function_est + log_sigmoid(function_est) 

        log_likelihood += (lambd*w.T.dot(w))

        return -1*log_likelihood*(1.0/float(n))

    def gradient(w):
        u = np.array([sigmoid(i) for i in X.dot(w)])
        return (X.T.dot(u-y) +2*lambd*w) + (1.0/float(n))

    def H(w):
        u = np.array([sigmoid(i) for i in X.dot(w)])
        S_k = np.diag(u - np.square(u))
        return (X.T.dot(S_k).dot(X) + 2*lambd*np.identity(m))*1.0/float(n)

    return objective, gradient, H

def get_classification_error(MAP, X_test, y_test):
    number_correct = 0
    for i in range(X_ctest.shape[0]):
        a = X_ctest[i].T.dot(w_map)
        prob = sigmoid(a)
        if prob > 0.5:
            pred = 1
        else:
            pred = 0

        if y_ctest[i] == pred:
            number_correct += 1

    return 1 - float(number_correct) / float(y_ctest.shape[0])


train = np.loadtxt("spam.train.dat")
test = np.loadtxt("spam.test.dat")

y_train = train[:, 57]
X_train = train[:, :57]
y_test = test[:, 57]
X_test = test[:, :57]

lambd = math.e**(-8)
objective, g, H = get_OGH(X_train, y_train, lambd)
grad = minimize(objective, np.zeros(58), method='Newton-CG', jac=g, hess=H)
MAP = grad.x
diff = np.linalg.norm(g(MAP) - approx_grad(objective, MAP, 0.000000001))

# Xs_without_repeat = []
# Xs = []
# ys_cross_err = []
# ys_test_err = []
# avg_cross_err = []
# avg_test_err = []
# for i in range(0,17):
#         print i
#         lambd = math.e**(i-8)
#         Xs_without_repeat.append(-(i-8))
#         for j in range(10):
#             Xs.append(-(i-8))

#         kf = cross_validation.KFold(3000, n_folds=10)

#         cross_err_sum = 0
#         test_error_sum = 0
#         for train_index, test_index in kf:
#             X_ctrain, X_ctest = X_train[train_index], X_train[test_index]
#             y_ctrain, y_ctest = y_train[train_index], y_train[test_index]

#             objective, g, H = get_OGH(X_train, y_train, lambd)            
#             res = minimize(objective, np.zeros(57), method='Newton-CG', jac=g, hess=H)
#             w_map = res.x

#             cross_err = get_classification_error(MAP, X_ctest, y_ctest)
#             test_error = get_classification_error(MAP, X_test, y_test)

#             cross_err_sum += cross_err
#             test_error_sum += test_error
#             ys_cross_err.append(cross_err)
#             ys_test_err.append(test_error)

#         avg_test_err.append(test_error_sum / 10)
#         avg_cross_err.append(cross_err_sum / 10)

# plt.plot(avg_cross_err, 'ro', label='Cross Validation Error')
# plt.plot(avg_test_err, 'ro', label='Test Error')
# plt.show()

print  MAP
print str(diff)

