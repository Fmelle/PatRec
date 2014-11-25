"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Predict similar users
"""

#===============================================================================
# Imports
#===============================================================================

import pandas as pd
import numpy as np
from KNN import doKNN

#===============================================================================
# SimilarUsers
#===============================================================================

class SimilarUsers(object):
    """ SimilarUsers finds similar users

    Parameters
    ----------
    usrData:    MxN DataFrame of N users each with M features
    """
    def __init__(s, usrData, KNN_K):
        s.usrData = usrData
        s.KNN_K = KNN_K

    def findSimilarUsers(s, usrId):
        """ Find the similar users for a given user`

        Parameters
        ----------
        usrId: user id to peform operation for
        """

        # TODO handle taking in user vector instead

        # Remove self if in user data
        otherUsrs = s.usrData
        if usrId in otherUsrs.index:
            otherUsrs = otherUsrs.drop(usrId)

        # Note need to transpose usrData to have users in cols 
        similarUsrs = doKNN(otherUsrs.T, s.usrData.ix[usrId,:], s.KNN_K)

        # Remove distance measure before passing on to predicter
        similarUsrs.drop('distance',1, inplace=True)
        similarUsrs = np.ravel(similarUsrs.values)

        return similarUsrs