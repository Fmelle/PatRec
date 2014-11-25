"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Perform validation based by predicting ratings based on similar users
"""

#===============================================================================
# Imports and set-up
#===============================================================================

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

#===============================================================================
# Script parameters
#===============================================================================

SAVE = True

#===============================================================================
# Model parameters
#===============================================================================

# Parameters
params = {}
params['userWeight'] = .7
params['knnK'] = 10
params['numPrincipalComp'] = 10

NOTES = "Parameters: " + str(params)

#===============================================================================
# Load data files
#===============================================================================

# Consts
usrFile = '../../ConvertedCSV/yelp_academic_dataset_user_reduced_top50.csv'
reviewFile = '../../ConvertedCSV/yelp_academic_dataset_review_reduced_top50.csv'

# Get user data files
usrData = pd.read_csv(usrFile, index_col = yr.USR_ID,
    usecols = yr.USR_FEATURES)

# Get review data
reviewData = pd.read_csv(reviewFile,
    index_col = [yr.USR_ID, yr.BIZ_ID], usecols = yr.REVIEW_FEATURES)

#===============================================================================
# Init model
#===============================================================================

print 'Running validation with:'
print 'params: ', params
print 'usrFile: ', usrFile
print 'reviewFile: ', reviewFile
print

# Init recommendation
predicter = yr.YelpRecommendation(usrData, reviewData,
        params['numPrincipalComp'], params['knnK'], params['userWeight'])

# Record results
counts = {'n':0, 'nPred':0, 'sqrE':0, 'off': [0,0,0,0,0]}

#===============================================================================
# Run trials
#===============================================================================

# Iter through all reviews
N = len(usrData.index)
i = 0
for usr in list(usrData.index):
    i+=1

    # Predict each rating
    usrReviews = reviewData.loc[usr]
    counts['n'] += len(usrReviews)
        
    # Get predictions
    prediction = predicter.predictRatings(usr)

    # Get predicted reviews
    intersectReviews = usrReviews.index.intersection(prediction.index)
    counts['nPred'] += len(intersectReviews)

    # Get the ratings which the user has already reviewed
    usrRatings = usrReviews.loc[intersectReviews]
    predictedRatings = prediction.loc[intersectReviews]

    # Calculate and record error
    err = (usrRatings - predictedRatings)**2
    counts['sqrE'] += sum(np.ravel(err.values))

    offErr = usrRatings - predictedRatings.apply(np.round)
    for x in offErr.values:
        counts['off'][int(abs(x))] += 1

    # Progress report
    print 'Finished (%d/%d):'%(i,N), counts

#===============================================================================
# Process and Save Results
#===============================================================================

# Mean sqr err
if counts['nPred'] != 0:
    counts['MSE'] = counts['sqrE'] / counts['nPred']
    print counts

outData = counts
outData['usrFile'] = usrFile
outData['reviewFile'] = reviewFile
t = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
outData['date'] = t

# Add notes on model parameters
outData['notes'] = NOTES

# Save at json by timestamp
if SAVE:
    fName = t + '.json'
    FP = open(fName,'w')
    json.dump(counts, FP, sort_keys=True, indent=2)
    FP.close()
    print 'Saved to ', fName
