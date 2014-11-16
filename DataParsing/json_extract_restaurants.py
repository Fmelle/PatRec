#!/usr/bin/python
            
import simplejson as json
obj  = json.load(open("yelp_academic_dataset_business_reduced.json"))
# There are 42153 businesses - 14303 restaurants = 27850 items to drop
for a in xrange(27850):
	# Iterate through the objects and remove non-restaurants
	for i in xrange(len(obj)):
		if not any('Restaurant' in s for s in obj[i]['categories']):
			obj.pop(i)
			break

# Output the updated file with pretty JSON
open("yelp_academic_dataset_business_reduced_restaurants.json", "w").write(
    json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
)