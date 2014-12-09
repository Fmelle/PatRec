# Test script to run with a specified user

import os

usr = 'ZrUZtLgLOn15v2NIZl-oKQ'
usrFile = '../ConvertedCSV/user_feature_matrix.csv'
reviewFile = '../ConvertedCSV/user_restaurant_review_mapping_ext.csv'
os.system(' '.join(['python','YelpRecommendation.py', usr, usrFile, reviewFile]))
