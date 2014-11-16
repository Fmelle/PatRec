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
import setup
from KNN import doKNN
from PredictRatings import PredictRatings
from PickRecommendation import PickRecommendation

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
        super(YelpRecommendation, self).__init__()
        s.usrData = usrData
        s.reviewData = reviewData

    def getRecommendation(s,usr):
        """
        Get a recommendation for the given user
        
        Parameters
        ----------
        usr:    User id
        """

        # Find similar users

        pass

        

#===============================================================================
# Main
#===============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide a recommendation ' +
        'for a given user')
    parser.add_argument('userName', metavar='usr', type=str,
        help='the user who wants a recommendation')
    parser.add_argument('userFile', metavar='usrF', type=str,
        help='the user data file')
    parser.add_argument('reviewFile', metavar='revF', type=str,
        help='the review data file')

    args = parser.parse_args()
    print 'Running Yelp Recommendation for ' + args.userName


