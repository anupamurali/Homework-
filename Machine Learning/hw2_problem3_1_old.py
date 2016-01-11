import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad as integrate
import matplotlib.pyplot as plt
import math
from sklearn import cross_validation

def approx_grad(obj, w, h) :
    res = np.zeros(w.shape)
    for i in range(res.size) :
        a = np.zeros(w.shape)
        a[i] = h
        res[i] = (obj(w+a) - obj(w-a)) / (2 * h)
    return res


def sigmoid_neg(a):
    return math.e**a / (math.e**a + 1)


def sigmoid_pos(a):
    return 1 / (1 + math.e**(-a))


def log_of_sigmoid_pos(a):
    return -1 * math.log(1 + math.e**(-a))


def log_of_sigmoid_neg(a):
    return a - math.log(1 + math.e**a)


def log_of_sigmoid(a):
    if a < 0:
        return log_of_sigmoid_neg(a)
    else:
        return log_of_sigmoid_pos(a)


def sigmoid(a):
    if a < 0:
        return sigmoid_neg(a)
    else:
        return sigmoid_pos(a)


# The objective, gradient, and Hessian functions
def obj_grad_and_hessian(X, y, l):
    def obj(w):
        ll = 0
        for i in range(X.shape[0]):
            datum = X[i]
            function_est = w.T.dot(datum)
            if y[i] == 1:
                ll += log_of_sigmoid(function_est)
            else:
                ll += (-function_est + log_of_sigmoid(function_est))

        ll += (l * w.T.dot(w))

        return -1 * ll * (1.0 / float(X.shape[0]))

    def grad(w):
        u = np.array([sigmoid(ele) for ele in X.dot(w)])
        return (X.T.dot(u - y) + 2 * l * w) * (1.0 / float(X.shape[0]))

    def hessian(w):
        u = np.array([sigmoid(ele) for ele in X.dot(w)])
        S = np.diag(u - np.square(u))
        return (X.T.dot(S).dot(X) + 2 * l * np.identity(X.shape[1])) * (1.0 / float(X.shape[0]))

    return obj, grad, hessian


def compute_basis_vector(x, D):
    vector = []
    for i in range(D):
        if i == 0:
            vector.append(1)
        else:
            vector.append(x**i)
    return vector


def normalize_features(X_train, X_test):
    mean_X_train = np.mean(X_train, 0)
    std_X_train = np.std(X_train, 0)
    std_X_train[ std_X_train == 0 ] = 1
    X_train_normalized = (X_train - mean_X_train) / std_X_train
    X_test_normalized = (X_test - mean_X_train) / std_X_train
    return X_train_normalized, X_test_normalized


def compute_design_vector(x, D):
    design_vector = []
    for i in range(10):
        arr = compute_basis_vector(x[i], D)
        design_vector.append(arr)

    return np.array(design_vector)

def get_classification_error(MAP, X_ctest, y_ctest):
    number_correct = 0
    for i in range(X_ctest.shape[0]):
        a = X_ctest[i].T.dot(MAP)
        prob = sigmoid(a)
        if prob > 0.5:
            pred = 1
        else:
            pred = 0

        if y_ctest[i] == pred:
            number_correct += 1

    return 1 - float(number_correct) / float(y_ctest.shape[0])


def main():
    train = np.loadtxt("spam.train.dat")
    test = np.loadtxt("spam.test.dat")

    y_train = train[:, 57]
    X_train = train[:, :57]
    y_test = test[:, 57]
    X_test = test[:, :57]

    # parameters
    l = math.e**-8

    #X_train, X_test = normalize_features(X_train, X_test)

    X_train = np.concatenate((X_train, np.ones((X_train.shape[0], 1))), 1)
    X_test = np.concatenate((X_test, np.ones((X_test.shape[0], 1))), 1)

    obj, grad, hessian = obj_grad_and_hessian(X_train, y_train, l)
    res = minimize(obj, np.zeros(58), method='Newton-CG', jac=grad, hess=hessian)
    w_map = res.x
    diff = np.linalg.norm(grad(w_map) - approx_grad(obj, w_map, 0.000000001))
    print w_map
    print "Norm of Difference from gradient in numerical approx: " + str(diff)

    Xs_without_repeat = []
    Xs = []
    ys_cross_err = []
    ys_test_err = []
    avg_cross_err = []
    avg_test_err = []
    for i in range(0,17):
        print i
        l = math.e**(i-8)
        Xs_without_repeat.append(-(i-8))
        for j in range(10):
            Xs.append(-(i-8))

        kf = cross_validation.KFold(3000, n_folds=10)

        cross_err_sum = 0
        test_error_sum = 0
        for train_index, test_index in kf:
            X_ctrain, X_ctest = X_train[train_index], X_train[test_index]
            y_ctrain, y_ctest = y_train[train_index], y_train[test_index]

            obj, grad, hessian = obj_grad_and_hessian(X_ctrain, y_ctrain, l)
            res = minimize(obj, np.zeros(58), method='Newton-CG', jac=grad, hess=hessian)
            w_map = res.x

            cross_err = get_classification_error(w_map, X_ctest, y_ctest)
            test_error = get_classification_error(w_map, X_test, y_test)

            cross_err_sum += cross_err
            test_error_sum += test_error
            ys_cross_err.append(cross_err)
            ys_test_err.append(test_error)

        avg_test_err.append(test_error_sum / 10)
        avg_cross_err.append(cross_err_sum / 10)

    plt.plot(avg_cross_err)
    plt.plot(avg_test_err)
    plt.show()


if __name__ == "__main__":
    main()