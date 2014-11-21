# Create histograms for stars

from collections import Counter
import pandas as pd
import numpy as np 
import pylab as plt

# Load data
reviewFile = '../ConvertedCSV/yelp_academic_dataset_review_reduced.csv'
reviewData = pd.read_csv(reviewFile, index_col = ['user_id', 'business_id'], usecols = ['user_id', 'business_id', 'stars'])

stars = np.ravel(reviewData.values)

# Create histograms
n, bins, patches = plt.hist(stars, 5, normed=1, histtype='bar', rwidth=0.8)
print n
plt.title('Number of reviews by stars')
plt.xlabel('Number of stars')
plt.ylabel('Number of reviews')
#plt.savefig('stars.png')
plt.show()