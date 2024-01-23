import os
import json

# def txt_to_json(input_file, output_file):
#     # Read the tab-separated text file with UTF-8 encoding
#     with open(input_file, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     # Extract header and data
#     header = lines[0].strip().split('\t')
#     data = [line.strip().split('\t') for line in lines[1:]]

#     # Create a list of dictionaries
#     json_data = [dict(zip(header, entry)) for entry in data]

#     # Write the JSON data to a file with UTF-8 encoding
#     with open(output_file, 'w', encoding='utf-8') as json_file:
#         json.dump(json_data, json_file, indent=2, ensure_ascii=False)

# # Specify your input and output file paths
# input_txt_file = './testset/posts_groundtruth.txt'
# output_json_file = './testset/posts_groundtruth.json'

# # Convert the text file to JSON
# txt_to_json(input_txt_file, output_json_file)

# exit()

def get_jpg_prefixes(folder_path):
    # Get the list of files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Extract prefixes from .jpg files
    jpg_prefixes = [os.path.splitext(file)[0] for file in files if file.lower().endswith('.jpg')]
   
    return jpg_prefixes

folder_path = "./Mediaeval2016_TestSet_Images"
prefix_list = get_jpg_prefixes(folder_path)

# for i,prefix in enumerate(prefix_list):
#     prefix_list[i] = './Mediaeval2016_TestSet_Images' + prefix + '.jpg'



print("Number of prefixes:", len(prefix_list))


def corpus(prefix_list, output_file='./twitter.json'):
    with open('./testset/posts_groundtruth.json', 'r', encoding='utf-8') as file:
        # Load JSON data from the file
        json_data = json.load(file)

    # Filter json_data based on the 'image_url' key
    filtered_data = []
    for data in json_data:
        if data['image_url'] in prefix_list and len(data['original_post']) > 100:
            data['image_url'] = 'twitter/Mediaeval2016_TestSet_Images/' + data['image_url'] + '.jpg'
            filtered_data.append(data)


    for i,d in enumerate(filtered_data):
        if d['label'] == 'real':
            d['label'] = 0
        else:
            d['label'] = 1


    # Write the filtered data to the output file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(filtered_data, output_file, indent=2, ensure_ascii=False)


corpus(prefix_list)
