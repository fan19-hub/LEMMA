import json
import random

json1 = 'out/twitter_lemma_base_kg_final_output_full.json'
json2 = 'out/twitter_lemma_test_kg_final_output_full.json'

with open(json1, 'r') as json_file:
    data1 = json.load(json_file)

with open(json2, 'r') as json_file:
    data2 = json.load(json_file)

match_count = 0

for ele in data1:
    for ele2 in data2:
        if ele['text'] == ele2['text']:
            if ele['prediction'] == ele2['prediction']:
                match_count += 1
                break

print(match_count)