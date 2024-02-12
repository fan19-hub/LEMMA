import json
import random
import time

import requests
from utils import stats, metric
from toolLearning import text_search
from lemma_component import LemmaComponent

if __name__ == '__main__':
    with open('out/fakereddit_lemma_base_kg_final_output_full_2.json', encoding='utf-8') as file:
        data = json.load(file)
    label = [item['label'] for item in data]
    prediction = [item['prediction'] for item in data]
    zero_shot = [item['direct'] for item in data]
    print(metric(label, prediction))
    print(metric(label, zero_shot))

