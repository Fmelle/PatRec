"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Predict users ratings for establishments they have not reviewed
"""

#===============================================================================
# Imports
#===============================================================================

import pandas as pd
import numpy as np

#===============================================================================
# PredictRatings
#===============================================================================

class PredictRatings(object):
    """
    Fill in missing user ratings based upon that users other ratings and the 
    overall establishment ratings.

    Parameters
    ----------
    knownRatings: Pandas Matrix Mx1 doubly indexed by user_id and business_id
                  with M being the number of reviews. Reviews are type float.
    """
    def __init__(s, knownRatings):
        s.knownRatings = knownRatings.sort()

    def getRatings(s, similarUsrs):
        """
        getRatings predicts ratings for the restaurants that similar
        users have visited

        Parameters
        ----------
        similarUsrs: Related users

        Returns
        -------
        Pandas matrix Mx1 with ratings
        """
        if len(similarUsrs) == 0:
            return []

        # Filter ratings to only look at similar users
        ratings = s.knownRatings.loc[pd.IndexSlice[similarUsrs,:],:]

        # Take mean of establishment reviews
        estMeans = ratings.mean(0, level='business_id')

        return estMeans


if __name__ == '__main__':
    print 'Running Predict User example'
    data = pd.read_csv('../Tests/rand_data_for_predict_ratings.csv', 
        index_col = ['user_id', 'business_id'])
    predictor = PredictRatings(data)
    print 'Data', data
    usrs = data.index.levels[0]
    similarUsrs = usrs[2:]
    print 'Predicted', predictor.getRatings(similarUsrs)
