import json
import random

# Assuming your JSON file is named 'data.json'
input_json_file = 'data/weibo/weibo.json'
output_json_file = 'data/weibo/weibo_shuffled.json'

# Read the JSON file
with open(input_json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Shuffle the data
random.shuffle(data)

# Save the shuffled data to a new JSON file
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f'Shuffled data has been saved to {output_json_file}')

      

    


