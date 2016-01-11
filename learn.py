import os
from collections import Counter
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import numpy as np
from scipy import sparse
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import util


# *******************************
#
# NOOB TRAIN AND TEST PAIR
#
# *******************************

learned_W = []


def majority_rule_ensemble(preds):
    num_classes = len(util.malware_classes)
    num_data = preds.shape[1]
    num_classifiers = preds.shape[0]
    output_preds = np.zeros(num_data)
    for n in xrange(num_data):
        votes = np.zeros(num_classes)
        for j in xrange(num_classifiers):
            votes[preds[j,n]] += 1
        output_preds[n] = int(np.argmax(votes))
    return output_preds

def noob_train(X_train, global_feat_dict, t_train, train_ids):
    global learned_W
    # Arguments:
    #   X_train = Design matrix
    #   global_feat_dict = Dictionary mapping features to column numbers.
    #   t_train = List of target class labels. t_train[i] = label for row i in X_train.
    #   train_ids = List of training data IDs in the order that they appear in X_train
    #            (train_ids[i] is for row i in X_train)
    # This function shouldn't return anything. Whatever it outputs should be stored in some global variable
    # defined in this file, which can then be called by noob_test.
    learned_W = np.random.random((len(global_feat_dict),len(util.malware_classes)))
    return

def noob_test(X_test, global_feat_dict, test_ids):
    # Arguments:
    #   X_test = Design matrix of test data
    #   global_feat_dict = Dictionary mapping features to column numbers
    #   test_ids = List of test data IDs in the order that they appear in X_test
    #             (test_ids[i] is for row i in X_test)
    # Returns:
    #     A list of predictions such that preds[i] contains the prediction for the data point with ID test_ids[i]
    preds = np.argmax(X_test.dot(learned_W),axis=1)
    return preds

logistic_model = LogisticRegression()

def logistic_regression(X_train, global_feat_dict, t_train, train_ids):
    logistic_model.fit(X_train, t_train)
    # with open("logistic_feat_weights.txt", 'w') as f:
    #     out = ""
    #     for c in xrange(len(util.malware_classes)):
    #         out += "CLASS " + util.malware_classes[c] + "\n\n"
    #         for feat in sorted(global_feat_dict.keys()):
    #             out += "    " + feat + ": " + str(logistic_model.coef_[c,global_feat_dict[feat]]) + "\n"
    #         out += "\n\n"
    #     f.write(out)
    #     # TODO SORT FEATURE WEIGHTS!!
    return

def logistic_test(X_test, global_feat_dict, test_ids):
    preds = logistic_model.predict(X_test)
    return preds



svm_model = svm.SVC()

def svm_train(X_train, global_feat_dict, t_train, train_ids):
    svm_model.fit(X_train, t_train)
    return

def svm_test(X_test, global_feat_dict, test_ids):
    preds = svm_model.predict(X_test)
    return preds


from sklearn.mixture import GMM
gmm_model = GMM(n_components=len(util.malware_classes))

def gmm_train(X_train, global_feat_dict, t_train, train_ids):
    gmm_model.fit(X_train)

def gmm_test(X_test, global_feat_dict, test_ids):
    preds = gmm_model.predict(X_test)
    return preds


randomforest_models = [RandomForestClassifier(n_estimators=i, max_depth=20) for i in xrange(10,35,5)]
#randomforest_models = [RandomForestClassifier(n_estimators=20)]

from sklearn import cross_validation

crossval_chosen_forest = -1
def crossval_randomforest_train(X_train, global_feat_dict, t_train, train_ids):
    global crossval_chosen_forest

    model_score = np.zeros(len(randomforest_models))
    num_folds = 3
    for i in xrange(len(randomforest_models)):
        scores = cross_validation.cross_val_score(randomforest_models[i], X_train.toarray(), t_train, cv=num_folds)
        model_score[i] = scores.mean()
    model_idx = int(np.argmax(scores))
    crossval_chosen_forest = model_idx
    randomforest_train(X_train, global_feat_dict, t_train, train_ids, id=crossval_chosen_forest)

def crossval_randomforest_test(X_test, global_feat_dict, test_ids):
    return randomforest_test(X_test, global_feat_dict, test_ids, id=crossval_chosen_forest)

def randomforest_train(X_train, global_feat_dict, t_train, train_ids, id=0):
    randomforest_models[id].fit(X_train.toarray(), t_train)
    return

def randomforest_test(X_test, global_feat_dict, test_ids, id=0):
    preds = randomforest_models[id].predict(X_test.toarray())
    return preds

from sklearn.naive_bayes import MultinomialNB

gauss_nb = MultinomialNB()
def naivebayes_train(X_train, global_feat_dict, t_train, train_ids):
    gauss_nb.fit(X_train.toarray(), t_train)
    return

def naivebayes_test(X_test, global_feat_dict, test_ids):
    preds = gauss_nb.predict(X_test.toarray())
    return preds

def ensemble_train(X_train, global_feat_dict, t_train, train_ids):
    svm_train(X_train, global_feat_dict, t_train, train_ids)
    logistic_regression(X_train, global_feat_dict, t_train, train_ids)
    for i in xrange(len(randomforest_models)):
        randomforest_train(X_train, global_feat_dict, t_train, train_ids, id=i)

def ensemble_test(X_test, global_feat_dict, test_ids):
    preds = []
    preds.append(svm_test(X_test, global_feat_dict, test_ids))
    for i in xrange(len(randomforest_models)):
        preds.append(randomforest_test(X_test, global_feat_dict, test_ids, id=i))
    preds.append(logistic_test(X_test, global_feat_dict, test_ids))
    preds = np.array(preds)
    preds = majority_rule_ensemble(preds)
    return preds


# TODO: Try making a classifier that trains different stuff on different parts of the data.
TRAINING_FUNCTION = crossval_randomforest_train

TESTING_FUNCTION = crossval_randomforest_test

