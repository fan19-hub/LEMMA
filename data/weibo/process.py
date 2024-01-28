import json

# Assuming your JSON file is named 'data.json' with a different encoding
input_json_file = 'data/weibo/weibo.json'
output_json_file = 'data/weibo/weibo_2.json'

# Read the JSON file with the existing encoding
with open(input_json_file, 'r') as file:
    data = json.load(file)

processed_data = []

for element in data:
    element['image'] = 'weibo/' + element['image'] + '.jpg'
    processed_data.append(element)
  
# Save the filtered data to a new JSON file
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=2)
      

    


