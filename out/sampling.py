import json
import random

# json2 = 'data/twitter/twitter.json'
# output_json_path = 'data/twitter/twitter_50.json'

json2 = 'data/fakereddit/FAKEDDIT.json'
output_json_path = 'data/fakereddit/FAKEDDIT_50_2.json'

# json2 = 'data/weibo/weibo_shuffled.json'
# output_json_path = 'data/weibo/weibo_50.json'

with open(json2, 'r') as json_file:
    data2 = json.load(json_file)

total = 50
sample = []

indices = list(range(len(data2)))
random.shuffle(indices)  # Shuffle the indices randomly

for i in indices:
    if data2[i]['label'] == 1:
        sample.append(data2[i])
        total -= 1
    
    if total == 0:
        break
    

with open(output_json_path, 'w') as json_file:
    json.dump(sample, json_file, indent=2)

print('done')
      


