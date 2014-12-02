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
from sklearn.neighbors import NearestNeighbors

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
        # +1 to account for self being closest
        s.nbrs = NearestNeighbors(n_neighbors=KNN_K+1, algorithm='auto').fit(usrData.values)

    def findSimilarUsers(s, usrId):
        """ Find the similar users for a given user

        Parameters
        ----------
        usrId: user to perform knn
        """

        # Perform KNN
        usrVect = s.usrData.ix[usrId,:]
        distances, similarUsrsInd = s.nbrs.kneighbors(usrVect)

        # Remove self as top similar user
        similarUsrsInd = similarUsrsInd[0][1:]
        similarUsrs = s.usrData.index[similarUsrsInd]
        return similarUsrs