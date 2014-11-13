"""
18-794 Project Proposal: Yelp Recommendations
Fridtjof Melle (fmelle), Gavi Adler (gya), Spencer Barton (sebarton)
Fall 2014

Runs code to generate Yelp Recommendations. Performs validation and 
outputs a recommendation
"""

# TODO input user name to get recommendation
# TODO output recommendation

#===============================================================================
# Imports
#===============================================================================

import argparse

#===============================================================================
# Yelp Recomendation
#===============================================================================

class YelpRecommendation(object):
    """ YelpRecommendation takes a user and retuns a recommendation. It relies
        upon a pre-filtered dataset of yelp users.
    """
    def __init__(self, arg):
        super(YelpRecommendation, self).__init__()
        self.arg = arg
        

#===============================================================================
# Main
#===============================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide a recommendation ' +
        'for a given user')
    parser.add_argument('userName', metavar='U', type=str,
        help='the user who wants a recommendation')

    args = parser.parse_args()
    print 'Running Yelp Recommendation for ' + args.userName

