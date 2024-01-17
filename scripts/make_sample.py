import os
import json
import random

def create_subset_json(input_file, output_file, samples_per_label):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Separate data into two lists based on 'label' value
    label_0_data = [entry for entry in data if entry['label'] == 0]
    label_1_data = [entry for entry in data if entry['label'] == 1]

    # Sample the specified number of entries for each label
    sampled_label_0 = random.sample(label_0_data, min(samples_per_label, len(label_0_data)))
    sampled_label_1 = random.sample(label_1_data, min(samples_per_label, len(label_1_data)))

    # Combine the sampled data
    subset_data = sampled_label_0 + sampled_label_1

    # Write the subset data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(subset_data, outfile, ensure_ascii=False, indent=2)


# Example usage:
input_json_file = 'test.json'
output_json_file = 'test_200.json'
samples_per_label = 100  # Set the desired number of samples for each label

create_subset_json(input_json_file, output_json_file, samples_per_label)