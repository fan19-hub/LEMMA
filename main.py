import json
from imgCaption import img2txt
from kg_generate_and_compare import kg_generate_and_compare
from zero_shot_prediction import zero_shot
from tool_learning import search

# mode
zero_shot_mode = True

# print the result
view = True

# automatic resume
resume = True

# dataset (twitter or weibo)
data_name = 'twitter'

# using image caption cache
using_cache = True

# max retry times
max_retry = 2

# tool learning
tool_learning = False

# image caption cache file name
image_caption_cache_name = 'image_captioning_cache.json'
tool_learning_cache_name = 'tool_learning_cache.json'

# input data file name
if data_name == 'twitter':
    input_file = 'test_twitter.json'
elif data_name == 'weibo':
    input_file = 'test.json'

# output file names
output_score = 'results'
output_result = 'kg_final_output'


if __name__ == '__main__':
    # Open the JSON file
    print('View:{}\nResume:{}\nUsing cache:{}\nMax retry:{}\nInput file:{}\nOutput score:{}\nOutput result:{}\n'
          .format(view, resume, using_cache, max_retry, input_file, output_score, output_result))

    with open(input_file, encoding='utf-8') as file:
        data = json.load(file)

    image_captioning_cache = {}
    tool_learning_cache = {}

    if using_cache:
        try:
            with open(image_caption_cache_name, encoding='utf-8') as f:
                image_captioning_cache = json.load(f)
            print('Using image captioning cache')
        except FileNotFoundError:
            image_captioning_cache = {}
            print('No image captioning cache found')
        try:
            with open(tool_learning_cache_name, encoding='utf-8') as f:
                tool_learning_cache = json.load(f)
            print('Using tool learning cache')
        except FileNotFoundError:
            tool_learning_cache = {}
            print('No tool learning cache found')

    if resume:
        with open(output_score, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = []
            for char in lines[1]:
                if char.isdigit():
                    labels.append(int(char))
            pred_labels = []
            for char in lines[3]:
                if char.isdigit():
                    pred_labels.append(int(char))
        results = []
        data = data[len(labels):]
        print('Resuming from index', len(labels))
    else:
        results = []
        pred_labels = []
        labels = []
        print('Starting from index 0')
        with open(output_score, 'w', encoding='utf-8') as f:
            f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        with open(output_result, 'w', encoding='utf-8') as f:
            f.write('')

    for item in data:
        print('Processing index {}/{}'.format(len(labels), len(data)))
        # read
        url = item["image_url"]
        text = item["original_post"]
        label = item["label"]

        # tool learning
        if tool_learning:
            print('Tool learning...')
            use_cache_flag = False
            if using_cache:
                if text in tool_learning_cache:
                    tool_learning_text = tool_learning_cache[text]
                    use_cache_flag = True

            if not use_cache_flag:
                for i in range(max_retry):
                    try:
                        tool_learning_text = search(text)
                        if tool_learning_text is None:
                            print('Tool learning error, retrying...')
                            continue
                        break
                    except:
                        print('Tool learning error, retrying...')
                else:
                    print('Tool learning error, skipping...')
                    continue
                if using_cache:
                    tool_learning_cache[text] = tool_learning_text
                    with open(tool_learning_cache_name, 'w', encoding='utf-8') as f:
                        json.dump(tool_learning_cache, f, ensure_ascii=False)
        else:
            tool_learning_text = None

        use_cache_flag = False
        # image captioning
        if using_cache:
            if url in image_captioning_cache:
                image_text = image_captioning_cache[url]
                if 'sorry' not in image_text and 'Sorry' not in image_text:
                    use_cache_flag = True

        if not use_cache_flag:
            for i in range(max_retry):
                try:
                    image_text = img2txt(url, data_name)
                    if 'sorry' in image_text.lower():
                        print('Image captioning error, retrying...')
                        continue
                    break
                except:
                    print('Image captioning error, retrying...')
            else:
                print('Image captioning error, skipping...')
                continue
            if using_cache:
                image_captioning_cache[url] = image_text
                with open(image_caption_cache_name, 'w', encoding='utf-8') as f:
                    json.dump(image_captioning_cache, f)

        # kg
        for i in range(max_retry):
            try:
                if zero_shot_mode:
                    kg1, kg2, kg3, prob, explain = zero_shot(text, image_text, tool_learning_text)
                else:
                    kg1, kg2, kg3, prob, explain = kg_generate_and_compare(text, image_text, tool_learning_text)
                break
            except:
                print('KG error, retrying...')
        else:
            print('KG error, skipping...')
            continue

        if prob < 0.6:
            pred_label = 0
        else:
            pred_label = 1

        pred_labels.append(pred_label)
        results.append(explain)
        labels.append(label)

        if view:
            print('Text:\n{}\nImage:\n{}\nTool:\n{}\nKG1:\n{}\nKG2:\n{}\nKG3:\n{}\nLabel: {}\nPrediction: {}\n'
                  .format(text, image_text, tool_learning_text, kg1, kg2, kg3, label, explain))

        with open(output_score, 'w', encoding='utf-8') as f:
            f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        with open(output_result, 'a', encoding='utf-8') as f:
            f.write('Text:\n{}\nImage:\n{}\nTool:\n{}\nKG1:\n{}\nKG2:\n{}\nKG3:\n{}\nLabel: {}\nPrediction: {}\n'
                    .format(text, image_text, tool_learning_text, kg1, kg2, kg3, label, explain))

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

    with open(output_score, 'w', encoding='utf-8') as f:
        f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        f.write('True positives: {}\n'.format(true_positives))
        f.write('False positives: {}\n'.format(false_positives))
        f.write('False negatives: {}\n'.format(false_negatives))
        f.write('True negatives: {}\n'.format(true_negatives))
        f.write('Precision: {}\n'.format(precision))
        f.write('Recall: {}\n'.format(recall))
        f.write('Accuracy: {}\n'.format(accuracy))
        f.write('F1 Score: {}\n'.format(f1_score))