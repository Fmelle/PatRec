"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Give an establishment recommendation for a given user
"""

#===============================================================================
# Imports
#===============================================================================

import sys
import pandas as pd
import numpy as np

#===============================================================================
# PickRecommendation
#===============================================================================

class PickRecommendation(object):
    """
    Given a user, a completed ratings prediction matrix give a recommendation

    Parameters
    ----------
    ratings: A completely filled ratings matrix between users and establishments
    """
    def __init__(s, ratings):
        # Perform deep copy so as not to destroy input dataFrame
        s.ratings = ratings.copy()

    def getRecommendation(s, usrId, usrReviewed):
        """
        getRecommendation creates a recommendation for the given user

        Algorithm
        ---------
        Picks the highest predicted user rating from establishments not yet
        reviewed.

        Parameters
        ----------
        usrId: User id string
        usrReviewed: List of business_id of reviewed establishments

        Returns
        -------
        Establishment names ordered by best recommendation to worst 
            or [] if no recommendation 
        """
        
        # Get possible recommendations
        unreviewed = np.setdiff1d(s.ratings.columns, usrReviewed,
            assume_unique=True)
        if len(unreviewed) == 0:
            return []

        # Get all users predicted recommendations
        usrRatings = s.ratings.loc[usrId, unreviewed]
        usrRatings.sort(ascending=False)
        # TODO cleaner way of extracting this data?
        return list(usrRatings.reset_index().ix[:,'business_id'])

if __name__ == '__main__':
    print 'Running Predict User example'

    data = pd.DataFrame.from_csv('../Tests/rand_data_for_pick_recommendation.csv')
    print data

    recommender = PickRecommendation(data)
    usr = {'name':'U1', 'reviewed':['R2', 'R3']}

    print recommender.getRecommendation(usr['name'], usr['reviewed'])
