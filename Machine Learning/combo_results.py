import csv
import numpy as np
import pylab as pl
import math
import pandas as pd
import matplotlib.pyplot as plt
import math

"""
Use Ridge Regression to compute a best fit line for data
"""

fname = 'train_rad2_bit1024.csv'
fname2 = 'test_rad2_bit1024.csv'
pred_filename  = 'combo_regression_rad2_bit1024.csv'

# data_offset = num_rows/2
train_df = pd.read_csv(fname)
test_df = pd.read_csv(fname2)
print test_df

X = np.array(train_df.drop('smiles', 1).drop('gap', 1))
Y = train_df['gap']

X_test = np.array(test_df.drop('smiles', 1))

alpha = 2

def ridge_regression(alpha):
	L = alpha*np.identity(X.shape[1])
	w = np.linalg.solve(np.dot(X.T, X) + np.dot(L.T, L) , np.dot(X.T, Y))
	results = np.dot(X_test, w)
	return alpha, w



# def hillclimb():
# 	olderror = 10000
# 	thresh = 0.01
# 	step = 0.001
# 	error = 0
# 	alpha = 1
# 	while olderror - error > thresh:
# 		print "TESTING ALPHA = ",alpha
# 		upalpha, upw = ridge_regression(alpha+step)
# 		downalpha, downw = ridge_regression(alpha-step)
# 		if uperror < downerror:
# 			alpha = upalpha
# 			error = uperror
# 			w = upw
# 		else:
# 			alpha = downalpha
# 			erorr = downerror
# 			w = downw
# 		error = min(uperror, downerror)
# 	return alpha, w

alpha = 0.948
_, w = ridge_regression(alpha)
results = np.dot(X_test, w)

# print train_df.drop('smiles', 1).drop('gap', 1)
# print sorted([x for x in xrange(256)], key=lambda x: abs(w[x]), reverse=True)
# print w
# quit()

# errors = np.zeros(data_offset)
# for i in xrange(data_offset):
# 	# print "Ridge regression gap prediction: ",results[i]
# 	# print "Actual gap = ", Y_test[i+data_offset]
# 	# print "ERROR = ",results[i] - Y_test[i+data_offset]
# 	# errors[i] = abs(float(100)*(results[i] - Y_test[i+data_offset])/float(Y_test[i+data_offset]))
# 	errors[i] = (results[i] - Y_test[i+data_offset])**2
# print "RMSE = ", math.sqrt(np.mean(errors))
# print "STD DEVIATION = ", np.std(errors)
# print "ALPHA: ", alpha


def test_prediction(Y_predict):
    deviations = Y_predict - Y_test
    return math.sqrt(np.dot(deviations, deviations) / len(deviations))


results_combo = np.ones(20)
n_estimators = 20
Y_predict_rfc = None
for max_features in range(10,11):
    for max_depth in range(39,40):
    
        rfc = RandomForestClassifier(n_estimators=n_estimators, max_depth = max_depth)#, max_features = max_features)
        rfc_model = rfc.fit(X,Y)
        Y_predict_rfc = rfc_model.predict(X_test)

        f = np.vectorize(lambda x: float(x))  # or use a different name if you want to keep the original f

        Y_predict_rfc = f(Y_predict_rfc)  # if A is your Numpy array
        #Y_predict_rfc = np.apply_along_axis(lambda x : float(x), 0, Y_predict_rfc)
        print 'rfc: ', test_prediction(Y_predict_rfc), 'n_estimators: ', n_estimators, 'max_depth: ', max_depth

 #   for weight_rfc in range(40,60):
  #      weight_rfc = weight_rfc/100.
   #     results_combo[weight_rfc] = test_prediction(weight_rfc*Y_predict_rfc + (1-weight_rfc)*results)


    results = 0.6*results + 0.4*Y_predict_rfc

# Write a prediction file.
with open(pred_filename, 'w') as pred_fh:

    # Produce a CSV file.
    pred_csv = csv.writer(pred_fh, delimiter=',', quotechar='"')

    # Write the header row.
    pred_csv.writerow(['Id', 'Prediction'])

    for i in xrange(len(results)):
        pred_csv.writerow([i+1, results[i]])

    
