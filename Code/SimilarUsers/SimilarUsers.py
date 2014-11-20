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

#===============================================================================
# SimilarUsers
#===============================================================================

class SimilarUsers(object):
	"""SimilarUsers"""
	def __init__(self, arg):
		self.arg = arg
		

		# TODO