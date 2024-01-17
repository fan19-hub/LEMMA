

Label1 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
Prediction1 = [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]

Label2 = 
[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
Prediction2 = 
[1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]

Label3 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Prediction3 = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1]

Labels4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
Predictions4 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0]


labels = Label1 + Label2 + Label3 + Labels4

pred_labels = Prediction1 + Prediction2 + Prediction3 + Predictions4

# with open('prediction.txt', 'r') as file:
#     # Read lines from the file and convert each line to an integer
#     pred_labels = [int(line.strip()) for line in file]

# with open('label.txt', 'r') as file:
#     # Read lines from the file and convert each line to an integer
#     labels = [int(line.strip()) for line in file]

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