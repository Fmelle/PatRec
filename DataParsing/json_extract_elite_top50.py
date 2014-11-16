#!/usr/bin/python                                                               
            
import simplejson as json
from operator import itemgetter

obj  = json.load(open("yelp_academic_dataset_user_reduced_elite.json"))
top = []
# There are total 20045 elite users - extract the top 50 by review count
nb_users = 50
obj.sort(key=itemgetter('review_count'))
for i in xrange(nb_users):
	top.append(obj[i+len(obj)-nb_users])
# Top to bottom
top.reverse()

# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_user_reduced_top50.json", "w").write(
    json.dumps(top, sort_keys=True, indent=4, separators=(',', ': '))
)