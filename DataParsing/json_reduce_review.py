#!/usr/bin/python                                                               
            
import simplejson as json

review_new = []
with open('yelp_academic_dataset_review.json') as fin:
    for line in fin:
        line_contents = json.loads(line)
        del line_contents['type']
        del line_contents['text']
        review_new.append(line_contents)
    
# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_review_reduced_notext.json", "w").write(
    json.dumps(review_new, sort_keys=True, indent=4, separators=(',', ': '))
)