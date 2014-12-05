"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Perform validation based by predicting ratings based on similar users
"""

#===============================================================================
# Imports and set-up
#===============================================================================

import argparse
parser = argparse.ArgumentParser(description = \
                    'Validate our Yelp prediction engine')
parser.add_argument('-d', '--debug', help='Debug mode',   action='store_true')
parser.add_argument('-s', '--save',  help='Save results', action='store_true')
parser.add_argument('-k', '--knnk',  help='K for KNN', type=int, required=True)
parser.add_argument('-c', '--pcomp', help='# principal components', type=int, required=True)
parser.add_argument('-w', '--weights', \
    help='weights for the user, similar users, and the establishment, in that order', \
    nargs='+', type=float, required=True)
parser.add_argument('-v', '--verbose',help='Print statements',action='store_true')
args = parser.parse_args()

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

SAVE = args.save
DEBUG = args.debug

#===============================================================================
# Model parameters
#===============================================================================

# Parameters
params = {}
params['weights'] = args.weights # [userWeight, simUserWeight, establishmentWeight]
params['knnK'] = args.knnk
params['numPrincipalComp'] = args.pcomp

NOTES = "Parameters: " + str(params)
NOTES += " This is a full feature matrix"

#===============================================================================
# Load data files
#===============================================================================

# Consts
usrFile = '../../ConvertedCSV/user_feature_matrix.csv'
testUsrFile = '../../ConvertedCSV/validation_users_feature.csv'
reviewFile = '../../ConvertedCSV/user_restaurant_review_mapping_ext.csv'

# Get user data files
usrData = pd.read_csv(usrFile, index_col = yr.USR_ID)
testUsr = pd.read_csv(testUsrFile, index_col = yr.USR_ID)

# Get review data
reviewData = pd.read_csv(reviewFile,
    index_col = [yr.USR_ID, yr.BIZ_ID], usecols = yr.REVIEW_FEATURES)

#===============================================================================
# Init model
#===============================================================================
if args.verbose:
    print 'Running validation with:'
    print 'params: ', params
    print 'usrFile: ', usrFile
    print 'testFile: ', testUsrFile
    print 'reviewFile: ', reviewFile
    print

# Init recommendation
predicter = yr.YelpRecommendation(usrData, reviewData,
        params['numPrincipalComp'], params['knnK'], params['weights'])

# Record results
counts = {'n':0, 'nPred':0, 'sqrE':0, 'off': [0,0,0,0,0,0]}

#===============================================================================
# Run trials
#===============================================================================

# Iter through all reviews
N = len(testUsr.index)
i = 0
for usr in list(testUsr.index):
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
    if args.verbose: print 'Finished (%d/%d):'%(i,N), counts

    if DEBUG: break

#===============================================================================
# Process and Save Results
#===============================================================================

# Mean sqr err
if counts['nPred'] != 0:
    counts['MSE'] = counts['sqrE'] / counts['nPred']
    if args.verbose: print counts

outData = counts
outData['numUsr'] = N
outData['usrFile'] = usrFile
outData['testUsrFile'] = testUsrFile
outData['reviewFile'] = reviewFile
t = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
outData['date'] = t

# Add notes on model parameters
outData['notes'] = NOTES
outData['params'] = str(params)

print params['weights'], ',', params['knnK'], ',', params['numPrincipalComp'], \
      ',', counts['MSE'], counts['off']

# Save at json by timestamp
if SAVE and not DEBUG:
    fName = t + '.json'
    FP = open(fName,'w')
    json.dump(counts, FP, sort_keys=True, indent=2)
    FP.close()
    if args.verbose: print 'Saved to ', fName
