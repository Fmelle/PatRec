#!/bin/env python

import pandas as pd
import numpy as np

elite_user_file = '../ConvertedCSV/yelp_academic_dataset_user_reduced_elite.csv'
restaurant_file = '../ConvertedCSV/yelp_academic_dataset_besuness_reduced_restaurants.csv'

elite_users = pd.DataFrame.from_csv('
