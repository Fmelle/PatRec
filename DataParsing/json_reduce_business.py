#!/usr/bin/python                                                               
            
import simplejson as json

business_new = []
with open('yelp_academic_dataset_business.json') as fin:
    for line in fin:
        line_contents = json.loads(line)
        del line_contents['full_address']
        del line_contents['hours']
        del line_contents['open']
        del line_contents['city']
        del line_contents['neighborhoods']
        del line_contents['longitude']
        del line_contents['state']
        del line_contents['latitude']
        del line_contents['attributes']
        del line_contents['type']
        business_new.append(line_contents)
    
# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_business_reduced.json", "w").write(
    json.dumps(business_new, sort_keys=True, indent=4, separators=(',', ': '))
)