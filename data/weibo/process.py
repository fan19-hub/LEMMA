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

for ele in data:
    if ele['label'] == "0":
        ele['label'] = 0
        ele['image'] = ele['image'][:6] + 'nonrumor_images/' + ele['image'][6:]
    elif ele['label'] == "1":
        ele['label'] = 1
        ele['image'] = ele['image'][:6] + 'rumor_images/' + ele['image'][6:]
  

# Save the shuffled data to a new JSON file
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f'Shuffled data has been saved to {output_json_file}')

      

    


