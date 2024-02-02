import base64
import json
import os

import openai
import requests
from openai import OpenAI

from config import data_root


def onlineImg_process(prompt, url, model="gpt-4-vision-preview", max_tokens=1000, temperature=0.1):

    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
          {
            "role": "user",
            "content": [
              {"type": "text", "text": prompt},
              {
                "type": "image_url",
                "image_url": {
                  "url": f"{url}",
                },
              },
            ],
          }
        ],
        max_tokens=max_tokens,
        temperature=temperature
      )
    return response.choices[0].message.content


def offlineImg_process(prompt, image_path, model="gpt-4-vision-preview", max_tokens=1000, temperature=0.1):
    api_key = os.getenv("OPENAI_API_KEY")

    # Encode function
    def encode_image(image_path):
        with open(data_root + image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return eval(response.text)["choices"][0]["message"]["content"]


def metric(labels, pred_labels):

    def confusion_matrix(truth, pred):
        tp = sum((l == 1 and p == 1) for l, p in zip(truth, pred))
        fp = sum((l == 0 and p == 1) for l, p in zip(truth, pred))
        fn = sum((l == 1 and p == 0) for l, p in zip(truth, pred))
        tn = sum((l == 0 and p == 0) for l, p in zip(truth, pred))

        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + tn) if tp + tn > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        return tp, fp, fn, tn, precision, recall, f1

    accuracy = sum((l == p) for l, p in zip(labels, pred_labels)) / len(labels)

    rumor_labels = labels
    rumor_pred_labels = pred_labels

    non_rumor_labels = [1 - l for l in labels]
    non_rumor_pred_labels = [1 - p for p in pred_labels]

    rumor_metrics = confusion_matrix(rumor_labels, rumor_pred_labels)
    non_rumor_metrics = confusion_matrix(non_rumor_labels, non_rumor_pred_labels)

    return {
        'labels': labels,
        'predictions': pred_labels,
        'accuracy': accuracy,
        'rumor': {
            'true_positives': rumor_metrics[0],
            'false_positives': rumor_metrics[1],
            'false_negatives': rumor_metrics[2],
            'true_negatives': rumor_metrics[3],
            'precision': rumor_metrics[4],
            'recall': rumor_metrics[5],
            'f1': rumor_metrics[6]
        },
        'non_rumor': {
            'true_positives': non_rumor_metrics[0],
            'false_positives': non_rumor_metrics[1],
            'false_negatives': non_rumor_metrics[2],
            'true_negatives': non_rumor_metrics[3],
            'precision': non_rumor_metrics[4],
            'recall': non_rumor_metrics[5],
            'f1': non_rumor_metrics[6]
        }
    }


def write_metric_result(file_name, data, mode='w', prefix=''):

    with open(file_name, mode, encoding='utf-8') as f:
        if prefix:
            f.write('{}\n'.format(prefix))
        f.write('Labels:\n{}\nPredictions:\n{}\n\n'.format(data['labels'], data['predictions']))

        f.write('Accuracy: {}\n\n'.format(data['accuracy']))

        f.write('Rumor Section:\n')
        f.write('True positives: {}\n'.format(data['rumor']['true_positives']))
        f.write('False positives: {}\n'.format(data['rumor']['false_positives']))
        f.write('False negatives: {}\n'.format(data['rumor']['false_negatives']))
        f.write('True negatives: {}\n'.format(data['rumor']['true_negatives']))
        f.write('Precision: {}\n'.format(data['rumor']['precision']))
        f.write('Recall: {}\n'.format(data['rumor']['recall']))
        f.write('F1 Score: {}\n\n'.format(data['rumor']['f1']))

        f.write('Non-rumor Section:\n')
        f.write('True positives: {}\n'.format(data['non_rumor']['true_positives']))
        f.write('False positives: {}\n'.format(data['non_rumor']['false_positives']))
        f.write('False negatives: {}\n'.format(data['non_rumor']['false_negatives']))
        f.write('True negatives: {}\n'.format(data['non_rumor']['true_negatives']))
        f.write('Precision: {}\n'.format(data['non_rumor']['precision']))
        f.write('Recall: {}\n'.format(data['non_rumor']['recall']))
        f.write('F1 Score: {}\n\n'.format(data['non_rumor']['f1']))


def stats(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    num_items = len(data)
    labels = []
    predictions = []
    zero_shot_predictions = []
    total_correct = 0
    total_incorrect = 0
    zero_shot_correct = 0
    zero_shot_incorrect = 0
    total_modified = 0
    total_modified_0_to_1 = 0
    total_modified_0_to_1_correct = 0
    total_modified_0_to_1_incorrect = 0
    total_modified_1_to_0 = 0
    total_modified_1_to_0_correct = 0
    total_modified_1_to_0_incorrect = 0
    total_unmodified = 0
    total_modified_correct = 0
    total_modified_incorrect = 0

    for item in data:
        labels.append(item['label'])
        predictions.append(item['prediction'])
        zero_shot_predictions.append(item['direct'])
        if item['label'] == item['direct']:
            if item['prediction'] != item['label']:
                total_incorrect += 1
                zero_shot_correct += 1
                total_modified += 1
                if item['direct'] == 0:
                    total_modified_0_to_1 += 1
                    total_modified_0_to_1_incorrect += 1
                else:
                    total_modified_1_to_0 += 1
                    total_modified_1_to_0_incorrect += 1
                total_modified_incorrect += 1
            else:
                total_correct += 1
                zero_shot_correct += 1
                total_unmodified += 1
        else:
            if item['prediction'] == item['label']:
                total_correct += 1
                zero_shot_incorrect += 1
                total_modified += 1
                if item['direct'] == 0:
                    total_modified_0_to_1 += 1
                    total_modified_0_to_1_correct += 1
                else:
                    total_modified_1_to_0 += 1
                    total_modified_1_to_0_correct += 1
                total_modified_correct += 1
            else:
                total_incorrect += 1
                zero_shot_incorrect += 1
                total_unmodified += 1

    print('Total items: {}'.format(num_items))
    print('Total correct: {}'.format(total_correct))
    print('Total incorrect: {}'.format(total_incorrect))
    print('Total Accuracy: {}'.format(total_correct / num_items))
    print('Zero-shot correct: {}'.format(zero_shot_correct))
    print('Zero-shot incorrect: {}'.format(zero_shot_incorrect))
    print('Zero-shot Accuracy: {}'.format(zero_shot_correct / num_items))
    print('Total modified: {}\n\t| 0 -> 1: {}\n\t\t| Correct: {}\n\t\t| Incorrect : {}\n\t| 1-> 0: {}\n\t\t| Correct: {}\n\t\t| Incorrect : {}'.format(total_modified, total_modified_0_to_1, total_modified_0_to_1_correct, total_modified_0_to_1_incorrect, total_modified_1_to_0, total_modified_1_to_0_correct, total_modified_1_to_0_incorrect))
    print('Total unmodified: {}'.format(total_unmodified))
    print('Total modified correct: {}'.format(total_modified_correct))
    print('Total modified incorrect: {}'.format(total_modified_incorrect))

if __name__ == '__main__':
    # stats('out/fakereddit_lemma_base_kg_final_output_50.json')
    stats('out/fakereddit_lemma_test_kg_final_output_50_5.json')
