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

import argparse
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
# Use all numeric features
USR_FEATURES = ['compliments.plain', 'compliments.more', 'compliments.cool',
                'compliments.profile', 'average_stars', 'review_count',
                'compliments.list', 'votes.cool', 'votes.funny',
                'compliments.writer', 'fans', 'compliments.cute',
                'compliments.photos', 'compliments.note', 'compliments.funny',
                'votes.useful', 'compliments.hot', USR_ID]
# Use only stars
REVIEW_FEATURES = [USR_ID, BIZ_ID, 'stars']

# KNN Consts
KNN_K = 5
N_PRINCIPAL_COMP = 2

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
    """
    def __init__(s, usrData, reviewData):
        # Perform PCA on user data
        usrs = usrData.index;
        reducedUsrDat = pca.transform_data(usrData.T, N_PRINCIPAL_COMP)
        reducedUsrDat.columns = usrs

        s.usrData = reducedUsrDat.T
        s.reviewData = reviewData
        s.similarUsrSearcher = SimilarUsers(s.usrData, KNN_K)
        s.predicter = PredictRatings(s.reviewData)

    def getRecommendation(s, usrId):
        """
        Get a recommendation for the given user
        
        Parameters
        ----------
        usrId:    User id string
        """

        #----- Find similar users ----

        similarUsrs = s.similarUsrSearcher.findSimilarUsers(usrId)

        #----- Predict user ratings ----

        ratings = s.predicter.getRatings(usrId, similarUsrs)

        #----- Pick best recommendation ----

        recommender = PickRecommendation(ratings)

        usrReviewed = s.reviewData.loc[usrId].index
        recommendation = recommender.getRecommendation(usrId, usrReviewed)
        return recommendation[0]

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
    usrData = pd.read_csv(args.userFile, index_col = USR_ID,
        usecols = USR_FEATURES)

    # Get review data
    reviewData = pd.read_csv(args.reviewFile,
        index_col = [USR_ID, BIZ_ID], usecols = REVIEW_FEATURES)

    # Run recommendation
    recommender = YelpRecommendation(usrData, reviewData)
    print recommender.getRecommendation(args.userId);