#!/usr/bin/python                                                               
            
import simplejson as json
obj  = json.load(open("yelp_academic_dataset_user_reduced.json"))                                                 
# There are total 252898 users and 20045 elite users
for a in xrange(232853):
	# Iterate through the objects and remove non-elite users  
	for i in xrange(len(obj)):
		if len(obj[i]["elite"]) == 0:
			obj.pop(i)
			break

# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_user_reduced_elite.json", "w").write(
    json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
)