#!/bin/env python

import pandas as pd
import numpy as np

elite_user_file = '../ConvertedCSV/yelp_academic_dataset_user_reduced_elite.csv'
restaurant_file = '../ConvertedCSV/yelp_academic_dataset_business_reduced_restaurants.csv'
review_file = '../ConvertedCSV/yelp_academic_dataset_review_reduced.csv'

user_ids = pd.DataFrame(pd.DataFrame.from_csv(elite_user_file).reset_index()['user_id'])
restaurant_ids = pd.DataFrame(pd.DataFrame.from_csv(restaurant_file).reset_index()['business_id'])
reviews = pd.DataFrame.from_csv(review_file).reset_index()[['user_id', 'business_id', 'stars']]
user_reviews = user_ids.merge(reviews)
user_restaurant_reviews = restaurant_ids.merge(user_reviews)

pd.DataFrame.to_csv(user_restaurant_reviews, 'user_restaurant_review_mapping.csv')
