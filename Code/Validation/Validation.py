# Perform validation based by predicting ratings based on similar users

# Fix path problem
import sys, os, json
sys.path.append(os.path.abspath('..'))

# Import project needs
import pandas as pd
import numpy as np
import YelpRecommendation as yr
from SimilarUsers.KNN import doKNN
from PredictRatings.PredictRatings import PredictRatings
from datetime import datetime

#--------------------------

# Parameters
USER_WEIGHT = .7
KNN_K = 10

NOTES = 'USER_WEIGHT: ' + str(USER_WEIGHT) + ', KNN_K: ' + str(KNN_K)

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
predicter = PredictRatings(reviewData, USER_WEIGHT)

# Record results
counts = {'n':0, 'nPred':0, 'sqrE':0, 'off': [0,0,0,0,0]}

#--------------------------
# TODO use YelpRecommendation

# Iter through all reviews
for usr in list(usrData.index):

    # Get similar users
    otherUsrs = usrData.drop(usr)
    similarUsrs = doKNN(otherUsrs.T, usrData.ix[usr,:], KNN_K)

    # Remove distance measure before passing on to predicter
    similarUsrs.drop('distance',1, inplace=True)
    similarUsrs = similarUsrs.loc[:,'userID'].values

    # Get other's review establishments
    # TODO cleanup
    otherReviews = reviewData.loc[pd.IndexSlice[similarUsrs,:],:]
    otherReviews = otherReviews.reset_index()
    otherReviews = otherReviews['business_id']
    otherReviews = otherReviews.unique()

    # Predict each rating
    usrReviews = reviewData.loc[usr]
    counts['n'] += len(usrReviews)

    # Get predicted reviews
    predictedReviews = usrReviews.index.intersection(otherReviews)
    counts['nPred'] += len(predictedReviews)
    
    # Perform prediction if it makes sense
    if len(predictedReviews) > 0:
        
        # Get predictions
        prediction = predicter.getRatings(usr, similarUsrs)

        usrRatings = usrReviews.loc[predictedReviews]
        predictedRatings = prediction.loc[predictedReviews]

        # Calculate and record error
        err = (usrRatings - predictedRatings)**2
        counts['sqrE'] += sum(np.ravel(err.values))

        offErr = usrRatings - predictedRatings.apply(np.round)
        for x in offErr.values:
            counts['off'][int(abs(x))] += 1

    print 'Finished:', counts

# MSE
if counts['nPred'] != 0:
    counts['MSE'] = counts['sqrE'] / counts['nPred']
    print counts

outData = counts
outData['usrFile'] = usrFile
outData['reviewFile'] = reviewFile
t = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
outData['date'] = t
outData['notes'] = NOTES

FP = open(t + '.json','w')
json.dump(counts, FP, sort_keys=True, indent=2)
FP.close()