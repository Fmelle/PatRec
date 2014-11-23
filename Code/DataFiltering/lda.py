#!/bin/env python

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def transform_data(pandas_matrix, num_components):
    model = PCA(n_components = num_components)
    #pandas matrix has feature vector in column, model expects it in a row
    #-->convert to numpy matrix and then transpose
    transformed_data = model.fit_transform(pandas_matrix.as_matrix().transpose())
    #transpose back to row-wise and return pandas data frame
    return pd.DataFrame(transformed_data.transpose())
