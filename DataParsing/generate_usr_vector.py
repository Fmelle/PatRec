#!/usr/bin/python                                                               
            
import pandas as pd
import numpy as np
import ast

data = pd.read_csv('user_restaurant_review_mapping_ext.csv', 
    index_col = ['user_id', 'business_id'])

categories = pd.read_csv('restaurant_types.csv', index_col=[0])
catNum  = [c[0] + '_num'  for c in categories.values]
catStar = [c[0] + '_star'  for c in categories.values]

usrs = data.index.levels[0]

indices = ['avg_stars', 'avg_price', 'avg_diff']
indices = indices + catNum + catStar

usrVect = pd.DataFrame(columns=usrs, index=indices)
usrVect = usrVect.fillna(0.0)

# Populate 
for usr in usrs:

	usrVect.loc['avg_stars',usr] = data.loc[usr].stars.values.mean()
	usrVect.loc['avg_price',usr] = data.loc[usr].price_range.values.mean()
	diff  = data.loc[usr].stars - data.loc[usr].average_stars
	usrVect.loc['avg_diff',usr]  = diff.values.mean()

	# Extract reviewed categories
	for row in data.loc[usr].iterrows():
		cats = ast.literal_eval(row[1].categories)
		for c in cats:
			usrVect.loc[c+'_num',usr] += 1
			usrVect.loc[c+'_star',usr] += row[1].stars

	# Make avg
	for i in xrange(len(catNum)):
		if usrVect.loc[catNum[i],usr] > 0:
			usrVect.loc[catStar[i],usr] = usrVect.loc[catStar[i],usr] / usrVect.loc[catNum[i],usr]

usrVect.to_csv('user_feature_matrix.csv')