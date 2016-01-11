import csv
import numpy as np
import pylab as pl
import math
import pandas as pd
import matplotlib.pyplot as plt
import math
from rdkit.Chem import AllChem

"""
Use Ridge Regression to compute a best fit line for data
"""

fname = 'train.csv'
fname2 = 'test.csv'
nfeatname  = 'train_rad3_bit4096_200k.csv'

# data_offset = num_rows/2
train_df = pd.read_csv(fname, nrows=150000)
test_df = pd.read_csv(fname2, nrows=150000)
# print test_df


X = np.array(train_df.drop('smiles', 1).drop('gap', 1))
Y = train_df['gap']
X_smiles = np.array(train_df['smiles'])

X_test = np.array(test_df.drop('smiles', 1).drop('Id',1))

with open(nfeatname, 'w') as nfeat_fh:

    # Produce a CSV file.
    nfeat_csv = csv.writer(nfeat_fh, delimiter=',', quotechar='"')

    # Write the header row.
    num_bits = 4096
    nfeat_csv.writerow(['smiles'] + ['feat_%04d' % i for i in xrange(1,num_bits+1)] + ['gap'])

    for i in xrange(150000):
        if i % 500 == 0:
            print i
        smiles = X_smiles[i]
        mol = AllChem.MolFromSmiles(smiles)

        feat_vector = AllChem.GetMorganFingerprintAsBitVect(mol, 3, nBits=num_bits, useFeatures=True)
        # print "FEATURES = ",feat_vector
        nfeat_csv.writerow([smiles] + list(feat_vector) + [Y[i]])


    
