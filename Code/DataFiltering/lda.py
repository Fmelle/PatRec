#!/bin/env python

import numpy as np
from sklearn.lda import LDA

def transform_data(pandas_matrix):
    model = LDA()
    #pandas matrix has feature vector in column, model expects it in a row
    #-->convert to numpy matrix and then transpose
    transformed_data = model.fit_transform(pandas_matrix.as_matrix().transpose())
    #transpose back to row-wise and return pandas data frame
    return pd.DataFrame(transformed_data.transpose())
