import os

import json
from imgCaption import img2txt
from kg_generate_and_compare import kg_generate_and_compare

if __name__ == '__main__':
    # Open the JSON file
    with open('exampleinput.json') as file:
        data = json.load(file)

    results = []
    pred_labels = []
    labels = []
    view = True
    for item in data:
        # read
        url = item["image_url"]
        text = item["original_post"]
        label = item["label"]
        # image captioning
        image_text = img2txt(url)
        # KG generation and compare
        kg, pred_label, explain = kg_generate_and_compare(text, image_text)
        pred_labels.append(pred_label)
        results.append(explain)
        labels.append(label)
        if view:
            print(explain)
            with open('kg_final_output', 'w', encoding='utf-8') as f:
                f.write('KG:\n' + kg + '\n' + 'Prediction:\n' + explain)

    # calculate accuracy
    correct = 0
    for i in range(len(labels)):
        if labels[i] == pred_labels[i]:
            correct += 1
    print('Accuracy: ', correct / len(labels))