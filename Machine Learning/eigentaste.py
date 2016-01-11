import numpy as np
import csv
import matplotlib.pyplot as plt
from demographic_groups import young_male

train_file = 'train.csv'
test_file  = 'test.csv'
soln_file  = 'global_median.csv'

# Load the training data.
train_data = {}
user_map = {}
artist_map = {}
user_unmap = {}
artist_unmap = {}
artists_to_users = {}
artists_to_users_plays = {}
i = 0
j = 0
k = 0
print "loading data ..."
with open(train_file, 'r') as train_fh:
    train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')
    next(train_csv, None)
    for row in train_csv:
        if k%1000 == 0:
            print "row = ",k
        user   = row[0]
        artist = row[1]
        plays  = int(row[2])
        if user in young_male:
            if artist not in artists_to_users:
                artists_to_users[artist] = {user: 1}
                artists_to_users_plays[artist] = 1

            elif user not in artists_to_users[artist]:
                artists_to_users[artist][user] = 1
                artists_to_users_plays[artist] += 1

            if i not in user_map and user not in user_unmap:
                user_map[i] = user
                user_unmap[user] = i
                i += 1

            if j not in artist_map and artist not in artist_unmap:
                artist_map[j] = artist
                artist_unmap[artist] = j
                j += 1

            if not user in train_data:
                train_data[user] = {}

            train_data[user][artist] = plays
        k += 1
        
