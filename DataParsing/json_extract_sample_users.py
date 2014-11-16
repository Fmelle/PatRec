#!/usr/bin/python                                                               
            
import simplejson as json
from random import randint

obj  = json.load(open("yelp_academic_dataset_user_reduced.json"))                                                 
sample = [];
# There are total 252898 users - for testing we will extract 2014 users
start_ind = randint(0,250000)
i = 1
n = 2015
while i < n:
	if len(obj[start_ind+i]["elite"]) == 0:
		sample.append(obj[start_ind+i])
	else:
		n += 1
	i += 1

# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_user_reduced_sample.json", "w").write(
    json.dumps(sample, sort_keys=True, indent=4, separators=(',', ': '))
)