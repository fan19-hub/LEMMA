import json
import random

input_file_path = './data/twitter/twitter.json'
output_file_path = './data/twitter/twitter_shuffled.json'


def shuffle_json_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Shuffle the data
    random.shuffle(data)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2) 

shuffle_json_file(input_file_path, output_file_path)
