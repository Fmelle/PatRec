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

    def getRecommendation(s, usr):
        """
        getRecommendation creates a recommendation for the given user

        Algorithm
        ---------
        Picks the highest predicted user rating from establishments not yet
        reviewed.

        Parameters
        ----------
        usr: User data

        Returns
        -------
        Establishment names ordered by best recommendation to worst 
            or None if no recommendation 
        """
        
        # Get possible recommendations
        reviewed = np.array(usr['reviewed'])
        unreviewed = np.setdiff1d(s.ratings.columns, reviewed,
            assume_unique=True)
        if len(unreviewed) == 0:
            return None

        # Get all users predicted recommendations
        usrRatings = s.ratings.loc[usr['name'],unreviewed]
        usrRatings.sort(ascending=False)
        return list(usrRatings.index)


if __name__ == '__main__':
    print 'Running Predict User example'

    data = pd.DataFrame.from_csv('../Tests/rand_data_for_pick_recommendation.csv')
    print data

    recommender = PickRecommendation(data)
    usr = {'name':'U1', 'reviewed':['R2', 'R3']}

    print recommender.getRecommendation(usr)
