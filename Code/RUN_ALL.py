# Test script to run with a specified user

import os

usr = 'JLM36sYWmouJAZ2knzst7A'
usrFile = '../ConvertedCSV/yelp_academic_dataset_user_reduced_top50.csv'
reviewFile = '../ConvertedCSV/yelp_academic_dataset_review_reduced_top50.csv'
os.system(' '.join(['python','YelpRecommendation.py', usr, usrFile, reviewFile]))
