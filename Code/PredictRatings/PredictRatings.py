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
    usrWeight: The weighting to apply to the user's average review when
                predicting. Note weights get normalized.
    simWeight: The weighting to apply to the user's similar user average review when
                predicting. Note weights get normalized.
    estWeight: The weighting to apply to the establishment's average rating
                when predicting. Note weights get normalized.
    """
    def __init__(s, knownRatings, usrWeight = .33, simWeight = .33, estWeight = .33):
        s.knownRatings = knownRatings.sort()
        totalWeight = usrWeight + simWeight + estWeight
        s.USR_WEIGHT = float(usrWeight) / totalWeight
        s.EST_WEIGHT = float(estWeight) / totalWeight
        s.SIM_WEIGHT = float(simWeight) / totalWeight

    def getRatings(s, usrId, similarUsrs):
        """
        getRatings predicts ratings for the restaurants that similar
        users have visited

        Parameters
        ----------
        usrId: user who we are predicting for
        similarUsrs: Related users

        Returns
        -------
        Pandas matrix Mx1 with ratings
        """
        if len(similarUsrs) == 0:
            return []

        # Get rid of users we don't have info for
        badUsrs = list();
        for user_id in similarUsrs:
            if user_id not in s.knownRatings.index:
                badUsrs.append(user_id)
        for user_id in badUsrs:
            similarUsrs = similarUsrs.drop(user_id)
        
        # Filter ratings to only look at similar users
        ratings = s.knownRatings.loc[pd.IndexSlice[similarUsrs,:],:]

        # Take mean of establishment reviews from sililar users
        similarMeans = ratings.mean(0, level='business_id')
        ratingsReset = ratings.reset_index()


        # Get establishment means over all users
        # TODO cleaner way?
        establishments = ratingsReset.loc[:,'business_id']
        establishments = establishments.unique()
        estRatings = s.knownRatings.loc[pd.IndexSlice[:,establishments],:]
        estMeans = estRatings.mean(0, level='business_id')
        establishmentUsrCounts = pd.crosstab([ratingsReset.user_id], \
                        [ratingsReset.business_id]).sum(0)

        if usrId in s.knownRatings.index:
            # Factor in the user's average rating
            usrAvg = s.knownRatings.loc[usrId,:].mean()
            prediction = similarMeans*s.SIM_WEIGHT + usrAvg*s.USR_WEIGHT + \
                         estMeans*s.EST_WEIGHT
            # If there are not enough similar users for that restaurant, discard
            # the similar users score
            for business_id in prediction.index:
                # if there aren't enough similar users or they are close to the
                # business mean, do not consider them
                if (establishmentUsrCounts.ix[business_id] < 3 or 
                    abs(similarMeans.ix[business_id].stars - \
                        estMeans.ix[business_id].stars) < .5):
                    prediction.ix[business_id] = \
                        usrAvg*.5 + estMeans.ix[business_id].stars*.5
        else:
            # User not in index so just predict on similar users
            prediction = similarMeans
        
        return prediction


if __name__ == '__main__':
    print 'Running Predict User example'
    data = pd.read_csv('../Tests/rand_data_for_predict_ratings.csv', 
        index_col = ['user_id', 'business_id'])
    predictor = PredictRatings(data)
    print '=== Data ==='
    print data
    usrs = data.index.levels[0]
    usr = usrs[0]
    similarUsrs = usrs[2:]
    print predictor.getRatings(usr, similarUsrs)
