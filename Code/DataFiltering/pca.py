#!/bin/env python

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def transform_data(data, num_components):
    """
    Perform pca on the data frame given, return a data frame of the data 
    projected onto num_components components.

    Parameters
    ----------
    data : pandas data frame where each column is a feature vector for a user
    num_components : the number of principal components to project the data onto

    Example:
    --------
    In [1]: data = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]]).transpose()
    In [2]: data = pd.DataFrame(data)
    In [3]: transform_data(data, 1)
    Out[3]:
              0         1         2         3         4         5
    0 -1.383406 -2.221898 -3.605304  1.383406  2.221898  3.605304
    """
    model = PCA(n_components = num_components)
    #pandas matrix has feature vector in column, model expects it in a row
    #-->convert to numpy matrix and then transpose
    transformed_data = model.fit_transform(data.as_matrix().transpose())
    #transpose back to row-wise and return pandas data frame
    return pd.DataFrame(transformed_data.transpose())
