import json
import random

file_path = "data/PHEME/phemeset.json"
output_file = "data/PHEME/PHEME_reshuffled.json"

with open(file_path, 'r', encoding='utf-8') as file:
    # Load JSON data from the file
    json_data = json.load(file)

count = 0 
c2 = 0

filtered_data = []
for event in json_data:
    count_true = 60
    count_false = 60
    for posts in json_data[event]:
        if posts['label'] == 0 and count_true <= 0:
            continue
        if posts['label'] == 1 and count_false <= 0:
            continue

        del posts['dep']
        
        posts['image'] = 'PHEME/images/' + posts['image']
        image_path  = posts.pop('image')
        posts['image_url'] = image_path

        text = posts.pop('text')
        posts['original_post'] = text
        
        
        filtered_data.append(posts)
        if posts['label'] == 1:
            count_false = count_false -1
        elif posts['label'] == 0:
            count_true = count_true -1

        if count_true <= 0 and count_false <= 0:
            break
        
random.shuffle(filtered_data)

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=2)