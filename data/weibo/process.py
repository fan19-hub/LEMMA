import json
import random

# Assuming your JSON file is named 'data.json'
input_json_file = 'data/weibo/weibo_shuffled.json'
output_json_file = 'data/weibo/weibo_50.json'

# Read the JSON file
with open(input_json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Shuffle the data
random.shuffle(data)

num = 50
sample = []

for ele in data:
    sample.append(ele)
    num  = num - 1
    if num == 0:
        break


# Save the shuffled data to a new JSON file
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(sample, file, ensure_ascii=False, indent=2)

print(f'Shuffled data has been saved to {output_json_file}')

      

    


