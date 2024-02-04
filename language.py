from langdetect import detect
from collections import Counter
import json
import random

json2 = 'data/twitter/twitter.json'
output_json_path = 'data/twitter/twitter_50_6.json'

with open(json2, encoding='utf-8') as file:
    data = json.load(file)

set = ['fr', 'es', 'tr', 'nl']
total = 20
sample = []

indices = list(range(len(data)))
random.shuffle(indices)  # Shuffle the indices randomly

for i in indices:
    lang = detect(data[i]['original_post'])
    if lang in set:
        sample.append(data[i])
        total -= 1

    if total == 0:
        break
    
with open(output_json_path, 'w') as json_file:
    json.dump(sample, json_file, indent=2)

print('done')
      

# element_count = Counter(set)

# # Print the count for each unique element
# for element, count in element_count.items():
#     print(f"{element}: {count}")