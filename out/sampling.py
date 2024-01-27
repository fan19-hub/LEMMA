import json
import random

json2 = 'data/twitter/twitter.json'
output_json_path = 'data/twitter/twitter_50.json'

with open(json2, 'r') as json_file:
    data2 = json.load(json_file)

total = 50
sample = []

indices = list(range(len(data2)))
random.shuffle(indices)  # Shuffle the indices randomly

for i in indices:
    print(i)
    sample.append(data2[i])
    
    if total == 0:
        break
    total -= 1

with open(output_json_path, 'w') as json_file:
    json.dump(sample, json_file, indent=2)

print('done')
      


