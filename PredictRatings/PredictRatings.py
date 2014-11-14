"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Predict users ratings for establishments they have not reviewed
"""

#===============================================================================
# Imports
#===============================================================================

import sys
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
    knownRatings: Pandas Matrix MxN with M being the number of users and N the
                 number of restaurants and type float
    """
    def __init__(s, knownRatings):
        # Perform deep copy so as not to destroy input dataFrame
        s.knownRatings = knownRatings.copy()

        # First remove users and establishments with no reviews
        s.knownRatings.dropna(axis=0, how='all', inplace=True)
        s.knownRatings.dropna(axis=1, how='all', inplace=True)

    def getRatings(s):
        """
        getRatings predicts all missing ratings

        Algorithm
        ---------
        Empty spaces are filled by taking the average of the user's other
        reviews and the establishment's other reviews.

        Returns
        -------
        Pandas matrix MxN with no NaN values
        """
        ratings = s.knownRatings

        # Take mean of rows and cols
        usrMeans = np.mean(ratings, axis=1)
        estMeans = np.mean(ratings, axis=0)

        # Get NaN locations
        missingIndx = np.where(ratings.isnull())

        # Replace all missing indeces with average of user and establishment avg
        # Iterates by row TODO learn multi-indexing
        for [ir,ic] in np.array(missingIndx).T:
            ratings.iloc[ir,ic] = .5*(usrMeans[ir] + estMeans[ic])

        return ratings


if __name__ == '__main__':
    print 'Running Predict User example'
    data = pd.DataFrame.from_csv('../Tests/rand_data_for_predict_ratings.csv')
    predictor = PredictRatings(data)
    print data
    print predictor.getRatings()
