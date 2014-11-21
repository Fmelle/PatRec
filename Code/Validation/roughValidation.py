# Very rough validation

# Fix path problem
import sys, os, json
sys.path.append(os.path.abspath('..'))

import pandas as pd
import numpy as np
import YelpRecommendation as yr
from SimilarUsers.KNN import doKNN
from PredictRatings.PredictRatings import PredictRatings
from datetime import datetime

#--------------------------

# Consts
usrFile = '../../ConvertedCSV/yelp_academic_dataset_user_reduced_top50.csv'
reviewFile = '../../ConvertedCSV/yelp_academic_dataset_review_reduced_top50.csv'

# Get user data files
usrData = pd.read_csv(usrFile, index_col = yr.USR_ID,
    usecols = yr.USR_FEATURES)

# Get review data
reviewData = pd.read_csv(reviewFile,
    index_col = [yr.USR_ID, yr.BIZ_ID], usecols = yr.REVIEW_FEATURES)

#--------------------------

# Init recommendation
predicter = PredictRatings(reviewData)

# Record results
counts = {'n':0, 'unable':0, 'sqrE':0, 'off': [0,0,0,0,0]}

#--------------------------

# Iter through all reviews
for usr in list(usrData.index):

    # Get similar users
    otherUsrs = usrData.drop(usr)
    similarUsrs = doKNN(otherUsrs.T, usrData.ix[usr,:], yr.KNN_K)

    # Remove distance measure before passing on to predicter
    similarUsrs.drop('distance',1, inplace=True)

    similarUsrs = similarUsrs.loc[:,'userID'].values

    # Get other's review establishments
    otherReviews = reviewData.loc[pd.IndexSlice[similarUsrs,:],:]
    otherReviews = otherReviews.reset_index()
    otherReviews = otherReviews['business_id']
    otherReviews = otherReviews.unique()

    # Predict each rating
    usrReviews = reviewData.loc[usr]
    for establishment in usrReviews.index:
        
        # Update count
        counts['n'] += 1

        # Check that establishment is amoung similar usrs, if not cannot predict
        if establishment not in otherReviews:
            counts['unable'] += 1
            continue

        # Remove review
        val = predicter.knownRatings.loc[usr,establishment].copy()
        predicter.knownRatings.loc[usr,establishment] = None
        
        # Predicted
        prediction = predicter.getRatings(usr, similarUsrs)
        
        # Get predictions for given user
        # TODO ensure usr always in ratings output (even if only one review)
        usrRatings = prediction.loc[usr]
        usrRatings.index = usrRatings.index.droplevel(0)

        # Update counts
        if establishment in usrRatings.index:
            err = val.values[0] - usrRatings.loc[establishment]
            counts['sqrE'] += err**2 
            off = int(abs(round(val.values) - round(usrRatings.loc[establishment])))
            counts['off'][off] += 1
        else:
            counts['unable'] += 1

        # Set back value
        predicter.knownRatings.loc[usr,establishment] = val
    print 'Finished:', counts

# MSE
if counts['n'] != counts['unable']:
    counts['MSE'] = counts['sqrE'] / (counts['n'] - counts['unable'])
print counts

outData = counts
outData['usrFile'] = usrFile
outData['reviewFile'] = reviewFile
t = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
outData['date'] = t

FP = open('../../Results/'+t + '.json','w')
json.dump(counts, FP, sort_keys=True, indent=2)
FP.close()