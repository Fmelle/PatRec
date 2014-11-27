#!/bin/env python

import pandas as pd
import numpy as np
import simplejson as json
import sys

elite_user_file = '../ConvertedCSV/yelp_academic_dataset_user_reduced_elite.csv'
user_restaurant_reviews_file = 'user_restaurant_review_mapping_ext.csv'
categories = json.load(open("../ExtractedJSON/yelp_academic_dataset_all_restaurant_categories.json"))


users = pd.DataFrame.from_csv(elite_user_file).reset_index()
mapper = pd.DataFrame.from_csv(user_restaurant_reviews_file).reset_index()

# Remove unecessary attributes
del users['yelping_since']
del users['compliments.plain']
del users['compliments.cute']
del users['compliments.more']
del users['compliments.profile']
del users['elite']
del users['name']
del users['compliments.list']
del users['compliments.writer']
del users['fans']
del users['compliments.photos']
del users['compliments.note']
del users['compliments.hot']
del users['compliments.cool']
del users['compliments.funny']
# New user vector removes votes and updates variable names to
# avoid confusion with individual reviews
del users['votes.cool']
del users['votes.funny']
del users['votes.useful']
users['user_review_count'] = users.get('review_count', 0)
del users['review_count']
users['user_average_stars'] = users.get('average_stars', 0)
del users['average_stars']

#################################################################
# EXTEND USER VECTORS WITH CATEGORIES
#
# Below is pseudo-code for doing the mapping of the user vectors
#
# 	After a couple of hours trying to hack this I have to give
#	in to my limited python syntax knowledge..
#
# 	Thoughts:
#		Given the complex indexing of csv files an option is to load
#		the JSON file instead to better handle the indexing and
#		retrieval of the categories etc
#
#		- Otherwise below is how I imagine we could do this -
# 			(although I believe there are far less computationally
#			expensive methods to do the mapping)
#

# This code does not index the CSVs correctly (users[user] etc)
# merely to make the (pseudo-)code more readable
for user in users.columns:
	# Initialize all categories for given user to zero
	# to assure all vectors have the same length
	# -- This will introduce a lot of zeros.. there are alternatives to this approach..
	for cat in categories:
		# As csv are are limited to two dimensions I use individual
		# columns for each number
		user[cat + '_nb_reviews'] = 0
		user[cat + '_avg_stars'] = 0
		# The below attribute is merely to keep track of the total
		# in order to update the average correctly on each iteration
		# using this approach and is deleted at the end
		user[cat + '_total_stars'] = 0
	# Loop through all reviews...
	for review in mapper.columns:
		# .. and look for all reviews for given user
		if user['user_id'] == review['user_id']:
			# For each review loop through all 240 categories
			# and update the values for categories that
			# the review contains (each review contains multiple categories)
			for cat in categories:
				if any(cat in s for s in review['categories']):
					user[cat + '_nb_reviews'] += 1
					user[cat + '_total_stars'] += review['stars']
					# And update the average stars given for category based on the above numbers
					user[cat + '_avg_stars'] = user[cat + '_total_stars']/user[cat + '_nb_reviews']

# REMARK: The above code does of course not run - but for visual purposes
# in a IDE/editor I have chosen to not comment the whole section
#
# ... It is also not tested in any way 
#
# 		("mind-dump" would be a fitting description)
#
#################################################################

users.set_index('user_id', inplace=True)
users.fillna(0, inplace=True)
users = users.transpose()

# Normalize stars
for user in users.columns:
    users[user].loc['user_average_stars'] /= 5
    # If we choose to normalize the stars then this will preferably be done for 
    # the category specific stars aswell
	for cat in categories:
		users[user].loc[cat + '_avg_stars'] /= 5

# Finally we would delete the total stars attribute
for cat in categories:
	del users[cat + '_total_stars']

# Normalize votes -- votes are removed in this updated vector
#for user in user.columns:
#    votes = users[user].loc['votes.cool':]
#    votes = votes/np.linalg.norm(votes)
#    users[user].loc['votes.cool':] = votes

# Introduce new .csv file / keep the old to maintain pipeline
users.to_csv('user_features_new.csv')
