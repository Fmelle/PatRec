# Create histograms for number of reviews per restaurant and number of reviews per user

from collections import Counter
import pandas as pd
import numpy as np 
import pylab as plt

# Load data
reviewFile = '../ConvertedCSV/yelp_academic_dataset_review_reduced.csv'
reviewData = pd.read_csv(reviewFile, index_col = ['user_id', 'business_id'], usecols = ['user_id', 'business_id', 'stars'])

# Extract counts
usrCnt = Counter(reviewData.index.labels[0]).values()
bizCnt = Counter(reviewData.index.labels[1]).values()

# Create histograms
plt.hist(usrCnt, 300)
plt.xlim([0,50])
plt.title('Number of users by review count')
plt.xlabel('Number of reviews')
plt.ylabel('Number of users')
plt.savefig('usrCnt.png')
plt.figure()

plt.hist(bizCnt, 400)
plt.xlim([0,200])
plt.title('Business of businesses by review count')
plt.xlabel('Number of reviews')
plt.ylabel('Number of businesses')
plt.savefig('bizCnt.png')