import json
from imgCaption import img2txt
from kg_generate_and_compare import kg_generate_and_compare

if __name__ == '__main__':
    # Open the JSON file
    with open('test.json', encoding='utf-8') as file:
        data = json.load(file)

    results = []
    pred_labels = []
    labels = []
    view = True
    for item in data[:1]:
        # read
        url = item["image_url"]
        text = item["original_post"]
        label = item["label"]
        if label == 0:
            label = 1
        else:
            label = 0
        # image captioning

        image_text = img2txt(url)
        # KG generation and compare
        kg, pred_label, explain = kg_generate_and_compare(text, image_text)
        pred_labels.append(pred_label)
        results.append(explain)
        labels.append(label)
        if view:
            print(explain)
            with open('kg_final_output', 'a', encoding='utf-8') as f:
                f.write('Text:\n{}\nImage:\n{}\nKG:\n{}\nLabel: {}\nPrediction: {}\n\n'.format(text, image_text, kg, label, explain))

    print('Labels:', labels)
    print('Predictions:', pred_labels)

    true_positives = sum((l == 1 and p == 1) for l, p in zip(labels, pred_labels))
    false_positives = sum((l == 0 and p == 1) for l, p in zip(labels, pred_labels))
    false_negatives = sum((l == 1 and p == 0) for l, p in zip(labels, pred_labels))
    true_negatives = sum((l == 0 and p == 0) for l, p in zip(labels, pred_labels))

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
    accuracy = (true_positives + true_negatives) / len(labels) if len(labels) != 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    print("Precision:", precision)
    print("Recall:", recall)
    print("Accuracy:", accuracy)
    print("F1 Score:", f1_score)
