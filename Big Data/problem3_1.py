import graphlab
import numpy as np

train_file = open("/Users/Anupa/Dropbox/train-mnist-dense-with-labels.data", "r")
test_file = open("/Users/Anupa/Dropbox/test-mnist-dense-with-labels.data", "r")

train = np.loadtxt(train_file, delimiter=',')
test = np.loadtxt(test_file, delimiter=',')
print "got data"


# data = graphlab.SFrame(train)
# test_data = graphlab.SFrame(test)
# training_data, validation_data = data.random_split(0.8)

print train.size()

print data