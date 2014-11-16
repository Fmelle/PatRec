#!/usr/bin/python                                                               
            
import simplejson as json

user_new = []
with open('yelp_academic_dataset_user.json') as fin:
    for line in fin:
        line_contents = json.loads(line)
        del line_contents['friends']
        del line_contents['type']
        user_new.append(line_contents)
    
# Output the updated file with pretty JSON                                      
open("yelp_academic_dataset_user_nofriends.json", "w").write(
    json.dumps(user_new, sort_keys=True, indent=4, separators=(',', ': '))
)