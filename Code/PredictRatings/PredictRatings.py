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

    def getRatings(s, usr, similarUsrs):
        """
        getRatings predicts all missing ratings

        Algorithm
        ---------
        Empty spaces are filled by taking the average of the user's other
        reviews and the establishment's other reviews.

        Parameters
        ----------
        usr: String for the usr that we wish to review
        similarUsrs: 

        Returns
        -------
        Pandas matrix MxN with no NaN values
        """

        # Filter ratings to only look at similar users
        indeces = np.append(similarUsrs, usr)
        ratings = s.knownRatings.loc[pd.IndexSlice[indeces,:],:]

        ratings = ratings.unstack()

        # Remove users and establishments with no reviews
        ratings.dropna(axis=0, how='all', inplace=True)
        ratings.dropna(axis=1, how='all', inplace=True)

        # Take mean of rows and cols
        usrMeans = np.mean(ratings, axis=1)
        estMeans = np.mean(ratings, axis=0)

        # Get NaN locations
        missingIndx = np.where(ratings.isnull())

        # Do this for nearest neighbors
        # Replace all missing indeces with average of user and establishment avg
        for [ir,ic] in np.array(missingIndx).T:
            ratings.iloc[ir,ic] = .5*(usrMeans[ir] + estMeans[ic])

        return ratings


if __name__ == '__main__':
    print 'Running Predict User example'
    data = pd.read_csv('../Tests/rand_data_for_predict_ratings.csv', 
        index_col = ['user_id', 'business_id'])
    predictor = PredictRatings(data)
    print 'Data', data
    usrs = data.index.levels[0]
    usr = usrs[0]
    similarUsrs = usrs[2:]
    print 'Predicted', predictor.getRatings(usr, similarUsrs)
