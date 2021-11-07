import json

import random

# data = {}
# data['people'] = []
# data['people'].append({
#     'name': 'Scott',
#     'website': 'stackabuse.com',
#     'from': 'Nebraska'
# })
# data['people'].append({
#     'name': 'Larry',
#     'website': 'google.com',
#     'from': 'Michigan'
# })
# data['people'].append({
#     'name': 'Tim',
#     'website': 'apple.com',
#     'from': 'Alabama'
# })

# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)


data = {}

with open('Sublinks.txt') as json_file:
    data = json.load(json_file)
    # print(len(data['SubThreads']))
    data['SubThreads'][0]['comments'] = []
    data['SubThreads'][0]['comments'].append({
        'comment':'comment'
    })

    i=0
    for idx, thred in enumerate(data['SubThreads']):
        
        print('_', idx, random.randrange(4))

    # print(data['SubThreads'][0]['link'])

print(len(data['SubThreads']))