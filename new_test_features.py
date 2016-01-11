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
nfeatname  = 'test_rad2_bit1024.csv'

# data_offset = num_rows/2
print "Loading CSV..."
test_df = pd.read_csv(fname2)
print "CSV loaded"
# print test_df


X = np.array(test_df.drop('smiles', 1).drop('Id', 1))
X_smiles = np.array(test_df['smiles'])
print "SHAPE: ", X_smiles.shape


with open(nfeatname, 'w') as nfeat_fh:

    # Produce a CSV file.
    nfeat_csv = csv.writer(nfeat_fh, delimiter=',', quotechar='"')

    # Write the header row.
    num_bits = 1024
    nfeat_csv.writerow(['smiles'] + ['feat_%04d' % i for i in xrange(1,num_bits+1)])

    for i in xrange(len(X_smiles)):
        if i % 500 == 0:
            print i
        smiles = X_smiles[i]
        mol = AllChem.MolFromSmiles(smiles)

        feat_vector = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=num_bits, useFeatures=True)
        # print "FEATURES = ",feat_vector
        nfeat_csv.writerow([smiles] + list(feat_vector))
