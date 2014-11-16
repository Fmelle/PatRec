#!/bin/env python

import pandas as pd
import numpy as np

elite_user_file = '../ConvertedCSV/yelp_academic_dataset_user_reduced_elite.csv'

users = pd.DataFrame.from_csv(elite_user_file).reset_index()

del users['yelping_since']
del users['compliments.plain']
del users['compliments.cute']
del users['compliments.more']
del users['compliments.profile']
del users['elite']
del users['review_count']
del users['name']
del users['compliments.list']
del users['compliments.writer']
del users['fans']
del users['compliments.photos']
del users['compliments.note']
del users['compliments.hot']
del users['compliments.cool']
del users['compliments.funny']

users.set_index('user_id', inplace=True)
users.fillna(0, inplace=True)
users = users.transpose()

#normalize
for user in users.columns:
    users[user].loc['average_stars'] /= 5
    votes = users[user].loc['votes.cool':]
    votes = votes/np.linalg.norm(votes)
    users[user].loc['votes.cool':] = votes

users.to_csv('user_features.csv')
