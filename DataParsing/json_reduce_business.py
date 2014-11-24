#!/usr/bin/python                                                               
            
import simplejson as json

i = 0
business_new = []
with open('yelp_academic_dataset_business.json') as fin:
    for line in fin:
        line_contents = json.loads(line)
        del line_contents['full_address']
        del line_contents['hours']
        del line_contents['open']
        del line_contents['neighborhoods']
        price_range = line_contents.get('attributes', None).get('Price Range', 0)
        line_contents['price_range'] = price_range
        line_contents['average_stars'] = line_contents.get('stars', 0)
        del line_contents['stars']
        del line_contents['attributes']
        del line_contents['type']
        business_new.append(line_contents)
    
# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_business_reduced.json", "w").write(
    json.dumps(business_new, sort_keys=True, indent=4, separators=(',', ': '))
)