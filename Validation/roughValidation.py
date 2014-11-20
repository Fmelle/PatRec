# Very rough validation
import sys
import os
sys.path.append(os.path.abspath('..'))
import setup
setup.setup('..')

import pandas as pd
import numpy as np
from YelpRecommendation import *

# Consts
usr = 'JLM36sYWmouJAZ2knzst7A'
usrFile = '../ConvertedCSV/yelp_academic_dataset_user_reduced_top50.csv'
reviewFile = '../ConvertedCSV/yelp_academic_dataset_review_reduced_top50.csv'

# Get user data files
usrData = pd.read_csv(usrFile, index_col = USR_ID,
    usecols = USR_FEATURES)

# Get review data
reviewData = pd.read_csv(reviewFile,
    index_col = [USR_ID, BIZ_ID], usecols = REVIEW_FEATURES)

# Run recommendation
recommender = YelpRecommendation(usrData, reviewData)

usrReviews = reviewData.loc[usr]

# Predict each rating
for establishment in usrReviews.index:

	# Remove review
	val = recommender.reviewData.loc[usr,establishment].copy()
	recommender.reviewData.loc[usr,establishment] = None
	prediction = recommender.predictRatings(usr);

	# Predicted
	usrRatings = prediction.loc[usr]
	usrRatings.index = usrRatings.index.droplevel(0)
	if establishment in usrRatings.index:
		print val.values, usrRatings.loc[establishment]

	recommender.reviewData.loc[usr,establishment] = val
