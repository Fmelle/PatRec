import pandas as pd
import numpy as np
import ast

restaurant_info = \
    pd.DataFrame.from_csv('user_restaurant_review_mapping_ext.csv')
types = restaurant_info['categories']
s = set()
for types in list(types.values):
    for single_type in ast.literal_eval(types):
        s.add(single_type)

type_df = pd.Series(np.array(list(s)))
type_df.to_csv('restaurant_types.csv')
