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
