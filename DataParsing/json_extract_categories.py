#!/usr/bin/python
            
import simplejson as json
obj  = json.load(open("yelp_academic_dataset_business_reduced_restaurants.json"))
cats = []
# Collect all categories into array
for i in xrange(len(obj)):
	for cat in obj[i]['categories']:
		if not any(cat in s for s in cats):
			cats.append(cat)

# Output the updated file with pretty JSON
open("yelp_academic_dataset_all_restaurant_categories.json", "w").write(
    json.dumps(cats, sort_keys=True, indent=4, separators=(',', ': '))
)