"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Runs code to generate Yelp Recommendations. Performs validation and 
outputs a recommendation
"""

#===============================================================================
# Imports
#===============================================================================

import argparse, sys
import pandas as pd
import numpy as np

# Import Our files
from SimilarUsers.SimilarUsers import SimilarUsers
import DataFiltering.pca as pca
from PredictRatings.PredictRatings import PredictRatings
from PickRecommendation.PickRecommendation import PickRecommendation

#===============================================================================
# Constants
#===============================================================================

# CSV Parsing Consts
USR_ID = 'user_id'
BIZ_ID = 'business_id'
# Use only stars
REVIEW_FEATURES = [USR_ID, BIZ_ID, 'stars']

#===============================================================================
# Yelp Recomendation
#===============================================================================

class YelpRecommendation(object):
    """ YelpRecommendation takes a user and retuns a recommendation. It relies
        upon a pre-filtered dataset of yelp users.

    Parameters
    ----------
    usrData:    MxN DataFrame of N users each with M features
    reviewData: Kx3 DataFrame of K reviews each consisting of an establishment 
                id, user id and digIt factor
    numPrplCmp: Number of principal components for PCA
    knnK:       KNN number of nearest neighbors to find
    weights:    1x3 vector for weights for predict ratings
                [userWeight, simUserWeight, establishmentWeight]
    """
    def __init__(s, usrData, reviewData, numPrplCmp=10, knnK=5, weights=[.5, .5, 0]):
        # Sanity check on number of principal components
        if numPrplCmp > len(usrData.columns):
            print "Trying to reduce user features from %d to %d features"\
                    %(len(usrData.columns), numPrplCmp)
            sys.exit(0)

        # TODO logger utility

        # Perform PCA on user data
        usrs = usrData.index;
        reducedUsrDat = pca.transform_data(usrData.T, numPrplCmp)
        reducedUsrDat.columns = usrs

        # Save data
        s.usrData = reducedUsrDat.T
        s.reviewData = reviewData
        s.similarUsrSearcher = SimilarUsers(s.usrData, knnK)
        s.predicter = PredictRatings(s.reviewData, weights[0], 
                        weights[1], weights[2])

    def predictRatings(s, usrId):
        """
        Predict ratings for the given user based off of their 
        similar users' reviews
        
        Parameters
        ----------
        usrId:    User id string
        """

        #----- Find similar users ----

        similarUsrs = s.similarUsrSearcher.findSimilarUsers(usrId)

        #----- Predict user ratings ----

        ratings = s.predicter.getRatings(usrId, similarUsrs)

        return ratings

    def getRecommendation(s, usrId):
        """
        Get a recommendation for the given user
        
        Parameters
        ----------
        usrId:    User id string
        """

        #----- Predict Ratings -------------

        ratings = s.predictRatings(usrId)

        #----- Pick best recommendation ----

        recommender = PickRecommendation(ratings)

        usrReviewed = s.reviewData.loc[usrId].index
        recommendation = recommender.getRecommendation(usrReviewed)

        names = pd.DataFrame.from_csv('../ConvertedCSV/restaurant_id_name_mapping.csv')
        print recommendation[0]
        name = names.ix[recommendation[0]]['name']

        return name

#===============================================================================
# Main
#===============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide a recommendation ' +
        'for a given user')
    parser.add_argument('userId', metavar='usr', type=str,
        help='the user who wants a recommendation')
    parser.add_argument('userFile', metavar='usrF', type=str,
        help='the user data file (csv)')
    parser.add_argument('reviewFile', metavar='revF', type=str,
        help='the review data file (csv)')
    args = parser.parse_args()

    print 'Running Yelp Recommendation for ' + args.userId

    # Get user data files
    usrData = pd.read_csv(args.userFile, index_col = USR_ID)

    # Get review data
    reviewData = pd.read_csv(args.reviewFile,
        index_col = [USR_ID, BIZ_ID], usecols = REVIEW_FEATURES)

    # Run recommendation
    recommender = YelpRecommendation(usrData, reviewData)
    print recommender.getRecommendation(args.userId);