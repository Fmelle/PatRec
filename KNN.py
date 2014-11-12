#/bin/env python

# KNN for user and feature vector
import sys
import pandas as pd
import numpy as np

def doKNN(user_features, new_user_features, K):
    """
    Take in an NxM DataFrame representing what N user's rankings 
    on m features and a 1xM DataFrame of what one user's rankings 
    on the same M features. Find that user's K nearest neighbors. 
    Return a Kx1 data frame of the ID of the nearest neighbors.

    Parameters
    ----------
    user_featurs: a NxM DataFrame where each column is named
                a usedID and each row is the rating that column's
                userID gave to that row's restaurant
    new_user_features: a Mx1 DataFrame where each column is a
                feature score
    K : the number of nearest neighbors to return. Must be less
                than or equal to N.
    """
    
    user_features = user_features.reset_index(drop=True).astype('float')
    new_user_features = new_user_features.reset_index(drop=True).astype('float')

    # Check that we are looking for fewer neighbors than we have neighbors
    if K > len(user_features.columns):
        print "Trying to find " + str(K) + " neighbors from " + \
            str(len(user_features.columns)) + " possible neighbors"
        sys.exit(0)
    
    # Check that matrix and vector have the same number of features
    if len(user_features) != len(new_user_features):
        print "Different number of features in given data and new user"
        sys.exit(0)

    distances = pd.DataFrame(columns=['userID', 'distance']);
    # Find distance from each user
    for user in user_features.columns:
        user_reviews = user_features[user]
        dis = np.linalg.norm(new_user_features.sub(user_reviews, axis=0))
        distances.loc[len(distances)] = [user, dis]

    distances.sort('distance', ascending=False, inplace=True)
    distances = distances.head(K)

    return distances


# do this if you're running this file alone, otherwise can import doKNN function
if __name__ == '__main__':
    user_features = pd.DataFrame.from_csv('rand_data_for_knn.csv')
    new_user_features = pd.DataFrame.from_csv('rand_data_for_knn_single_user.csv')
    K = 5
    distances = doKNN(user_features, new_user_features, K)
