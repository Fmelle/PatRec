"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Runs code to generate Yelp Recommendations. Performs validation and 
outputs a recommendation
"""

# TODO make reviews doc smaller

#===============================================================================
# Imports
#===============================================================================

import argparse
import pandas as pd
import numpy as np


# Import Our files
import setup
from KNN import doKNN
from PredictRatings import PredictRatings
from PickRecommendation import PickRecommendation

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
        s.usrData = usrData
        s.reviewData = reviewData
        s.KNN_K = KNN_K
        s.predicter = PredictRatings(reviewData)

    def getRecommendation(s, usr):
        """
        Get a recommendation for the given user
        
        Parameters
        ----------
        usr:    User id
        """

        #----- Find similar users ----

        # Remove self if in user data
        otherUsrs = s.usrData
        if usr in otherUsrs.index:
            otherUsrs = otherUsrs.drop(usr)

        # Note need to transpose usrData to have users in cols 
        similarUsrs = doKNN(otherUsrs.T, s.usrData.ix[usr,:], s.KNN_K)

        # Remove distance measure before passing on to predicter
        similarUsrs.drop('distance',1, inplace=True)

        #----- Predict user ratings ----

        s.predicter.getRatings(usr, similarUsrs)

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

    # Debugging
    # print usrData.head()
    # print reviewData.head()

    # Run recommendation
    recommender = YelpRecommendation(usrData, reviewData)
    recommender.getRecommendation(args.userId);