import json
from imgCaption import img2txt
from KGprocess import kg_generate_and_compare
from cot import cot
from zero_shot import zero_shot
from toolLearning import search
from lemma import lemma
from config import data_root,out_root
from utils import metric, write_metric_result

# mode ('direct' or 'cot' or 'cot+kg' or 'cot+fact' or 'lemma')
#### EXPLAINATION ####
# direct: directly use the text and image as input
# cot: use chain of thought method 
# cot+kg: use chain of thought method and knowledge graph based reasoning
# cot+fact: use chain of thought method and fact check
# lemma: our method
mode = 'lemma'

# print the result
view = False

# automatic resume
resume = False

# dataset (twitter or weibo or fakereddit or ticnn)
data_name = 'twitter'

# using image caption cache
using_cache = True

# max retry times
max_retry = 5

# image caption cache file name
image_caption_cache_name = data_root+'image_captioning_cache.json'
tool_learning_cache_name = data_root+'tool_learning_cache.json'

# input data file name
if data_name == 'twitter':
    input_file = data_root+'twitter/twitter_s_50.json'
elif data_name == 'weibo':
    input_file = data_root+'test.json'
elif data_name == 'fakereddit':
    input_file = data_root+'fakereddit/FAKEDDIT.json'
elif data_name == 'ticnn':
    input_file = data_root+'ticnn/ticnn_sample.json'
elif data_name == 'fakehealth':
    input_file = data_root+'fakehealth/fakehealth.json'

# input_file=data_root+"exampleinput.json"

# output file names
output_score = out_root + data_name + '_' + mode + '_' + 'results_50'
output_result = out_root + data_name + '_' + mode + '_' + 'kg_final_output_50.json'

if __name__ == '__main__':
    # Open the JSON file
    print('View:{}\nResume:{}\nUsing cache:{}\nMax retry:{}\nInput file:{}\nOutput score:{}\nOutput result:{}\n'
          .format(view, resume, using_cache, max_retry, input_file, output_score, output_result))

    with open(input_file, encoding='utf-8') as file:
        data = json.load(file)

    image_captioning_cache = {}
    tool_learning_cache = {}

    all_results = []

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
        with open(output_result, 'r', encoding='utf-8') as f:
            all_results = json.load(f)
        data = data[len(labels):]
        print('Resuming from index', len(labels))
    else:
        pred_labels = []
        labels = []
        print('Starting from index 0')
        with open(output_score, 'w', encoding='utf-8') as f:
            f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        with open(output_result, 'w', encoding='utf-8') as f:
            f.write('')

    if mode == 'lemma':
        zero_shot_labels = []

    for item in data:
        print('Processing index {}/{}'.format(len(labels), len(data)))
        # read
        url = item["image_url"]
        text = item["original_post"]
        label = item["label"]

        # tool learning
        if mode == 'lemma' or mode == 'cot+fact':
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
                    except Exception as e:
                        print('Tool learning error: ', end="")
                        print(e)
                        print(",retrying...")
                else:
                    print('Tool learning error, skipping...')
                    continue
                if using_cache:
                    tool_learning_cache[text] = tool_learning_text
                    with open(tool_learning_cache_name, 'w', encoding='utf-8') as f:
                        json.dump(tool_learning_cache, f, ensure_ascii=False)
        else:
            tool_learning_text = None

        
        # image captioning
        if mode != 'direct' and mode != 'cot':
            use_cache_flag = False
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
                    except Exception as e:
                        print('Image captioning error:',end="")
                        print(e,end="")
                        print(",retrying...")
                else:
                    print('Image captioning error, skipping...')
                    continue
                if using_cache:
                    image_captioning_cache[url] = image_text
                    with open(image_caption_cache_name, 'w', encoding='utf-8') as f:
                        json.dump(image_captioning_cache, f)
        else:
            image_text = None

        # kg
        zero_shot_pred = None
        for i in range(max_retry):
            try:
                if mode == 'direct':
                    kg1, kg2, kg3, prob, explain = zero_shot(text, url)
                elif mode == 'cot':
                    kg1, kg2, kg3, prob, explain = cot(text, url)
                elif mode == 'cot+fact':
                    pass
                elif mode == 'lemma':
                    _, _, _, zero_shot_pred, _ = zero_shot(text, url)
                    kg1, kg2, kg3, prob, explain = lemma(text, url, image_text, tool_learning_text, zero_shot_pred)
                else:
                    kg1, kg2, kg3, prob, explain = kg_generate_and_compare(text, image_text, tool_learning_text)
                break
            except Exception as e:
                print('KG error: ',end="")
                print(e,end="")
                print(",retrying...")
        else:
            print('KG error, skipping...')
            continue

        if prob < 0.6:
            pred_label = 0
        else:
            pred_label = 1

        pred_labels.append(pred_label)
        labels.append(label)
        if zero_shot_pred is not None:
            zero_shot_labels.append(zero_shot_pred)

        all_results.append({
            'text': text,
            'image': url,
            'image_text': image_text,
            'tool_learning_text': tool_learning_text,
            'text_kg': kg1,
            'image_kg': kg2,
            'tool_kg': kg3,
            'label': label,
            'prediction': pred_label,
            'explain': explain,
            'direct': zero_shot_pred
        })

        if view:
            print('Text:\n{}\nImage:\n{}\nTool:\n{}\nKG1:\n{}\nKG2:\n{}\nKG3:\n{}\nLabel: {}\nPrediction: {}\n'
                  .format(text, image_text, tool_learning_text, kg1, kg2, kg3, label, explain))

        with open(output_score, 'w', encoding='utf-8') as f:
            f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        with open(output_result, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)

    evaluation_result = metric(labels, pred_labels)
    print('Evaluation result:', evaluation_result)
    write_metric_result(output_score, evaluation_result)

    if mode == 'lemma':
        evaluation_result = metric(labels, zero_shot_labels)
        print('Zero-shot evaluation result:', evaluation_result)
        write_metric_result(output_score, evaluation_result, 'a', prefix='zero shot section')
