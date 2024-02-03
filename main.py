import json
from imgCaption import img2txt
from KGprocess import kg_generate_and_compare
from cot import cot
from kg import kg_gen
from time import sleep
from question_gen import question_gen
from zero_shot import zero_shot
from toolLearning import text_search, visual_search
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
mode = 'lemma_base'

# print the result
view = True

# automatic resume
resume = False

# zero-shot conditional result
zs_flag = True

# dataset (twitter or weibo or fakereddit or ticnn)
data_name = 'twitter'

# using image caption cache
using_cache = True

# max retry times
max_retry = 5

# image caption cache file name
image_caption_cache_name = data_root+'image_captioning_cache.json'
tool_learning_cache_name = data_root+'tool_learning_cache.json'
kg_cache_name = data_root+'kg_cache.json'

# input data file name
if data_name == 'twitter':
    input_file = data_root+'twitter/twitter_50_3.json'
    use_online_image = True
elif data_name == 'weibo':
    input_file = data_root+'weibo/weibo_50.json'
    use_online_image = False
elif data_name == 'fakereddit':
    input_file = data_root+'fakereddit/FAKEDDIT_50.json'
    use_online_image = True
elif data_name == 'ticnn':
    input_file = data_root+'ticnn/ticnn_sample.json'
    use_online_image = True
elif data_name == 'fakehealth':
    input_file = data_root+'fakehealth/fakehealth.json'
    use_online_image = True

# input_file=data_root+"exampleinput.json"
# use_online_image=True

# output file names
output_score = out_root + data_name + '_' + mode + '_' + 'results_50_6'
output_result = out_root + data_name + '_' + mode + '_' + 'kg_final_output_50_6.json'

if __name__ == '__main__':
    # Open the JSON file
    configs = {
        "Dataset": data_name,
        "Image loading": "load from GitHub" if use_online_image else "load locally",
        "View": view,
        "Resume": resume,
        "Max retry": max_retry,
        "Input file": input_file,
        "Output score": output_score,
        "Output result": output_result,
        "Using cache": using_cache
    }
    print("Running LEMMa with mode:", mode)
    config_str = "\n".join([f" ├─ {k}: {v}" if k != "Using cache" else f" └─ Using cache: {v}"
                            for k, v in configs.items()])
    print(config_str)

    with open(input_file, encoding='utf-8') as file:
        data = json.load(file)

    image_captioning_cache = {}
    tool_learning_cache = {}

    all_results = []

    if using_cache:
        try:
            with open(image_caption_cache_name, encoding='utf-8') as f:
                image_captioning_cache = json.load(f)
            print(f'\t├─ Using image captioning cache: {image_caption_cache_name}')
        except FileNotFoundError:
            image_captioning_cache = {}
            print(f'\t├─ No image captioning cache found')
        try:
            with open(tool_learning_cache_name, encoding='utf-8') as f:
                tool_learning_cache = json.load(f)
            print(f'\t├─ Using tool learning cache: {tool_learning_cache_name}')
        except FileNotFoundError:
            tool_learning_cache = {}
            print(f'\t├─ No tool learning cache found')
        try:
            with open(kg_cache_name, encoding='utf-8') as f:
                kg_cache = json.load(f)
            print(f'\t└─ Using kg cache: {kg_cache_name}\n')
        except FileNotFoundError:
            kg_cache = {}
            print(f'\t└─ No kg cache found\n')

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
        total_data_size = len(data)
        data = data[len(labels):]
        print('Resuming from index', len(labels))
    else:
        pred_labels = []
        labels = []
        total_data_size = len(data)
        print('Starting from index 0')
        with open(output_score, 'w', encoding='utf-8') as f:
            f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        with open(output_result, 'w', encoding='utf-8') as f:
            f.write('')

    if mode.startswith('lemma'):
        zero_shot_labels = []

    for item in data:
        print('Processing index {}/{}'.format(len(labels), total_data_size))
        # read
        url = item["image_url"]
        text = item["original_post"]
        label = item["label"]
        zero_shot_pred = None

        if mode.startswith('lemma'):
            print('Zero shot...')
            for i in range(max_retry):
                try:
                    _, _, _, zero_shot_pred, _ = zero_shot(text, url, is_url=use_online_image)
                    break
                except Exception as e:
                    print(f'Zero shot error: {e}, retrying...')
            else:
                print('Zero shot error, skipping...')
                continue
        
        ## If zero-shot predict 0, zs_flag True

        if zero_shot_pred == 0:
            zs_flag= True
        elif zero_shot_pred == 1:
            zs_flag = False

    
        if mode.startswith('lemma'):
            use_cache_flag = False
            if using_cache:
                if text in tool_learning_cache:
                    use_cache_flag = True

            if not use_cache_flag:
                print('Generating Tool Learning Searching Questions...')
                for i in range(max_retry):
                    try:
                        res = question_gen(text, url, zero_shot_pred, is_url=use_online_image)
                        title = res['title']
                        questions = res['questions']
                        break
                    except Exception as e:
                        print(f'Question gen error: {e}, retrying...')
                else:
                    print('Question gen error, skipping...')
                    continue

        # tool learning
        if mode.startswith('lemma') or mode == 'cot+fact':
            print('Tool learning...')
            use_cache_flag = False
            if using_cache:
                if text in tool_learning_cache:
                    tool_learning_text = tool_learning_cache[text]
                    use_cache_flag = True
                    print('Retrieved tool learning result from cache')

            if not use_cache_flag:
                for i in range(2):
                    try:
                        tool_learning_text = text_search(text[:480], fake_news_prefix=not zero_shot_pred)
                        # tool_learning_text += visual_search(url, text)
                        if mode.startswith('lemma'):
                            tool_learning_text += text_search(title, fake_news_prefix=not zero_shot_pred)
                            for question in questions:
                                tool_learning_text += text_search(question, fake_news_prefix=not zero_shot_pred)
                                sleep(5)
                        if tool_learning_text is None:
                            print('Tool learning error, retrying...')
                            sleep(60)
                            continue
                        break
                    except Exception as e:
                        print(f'Tool learning error: {e}, retrying')
                        sleep(60)
                else:
                    print('Tool learning error, skipping...')
                    continue
                if using_cache:
                    tool_learning_cache[text] = tool_learning_text
                    with open(tool_learning_cache_name, 'w', encoding='utf-8') as f:
                        json.dump(tool_learning_cache, f, ensure_ascii=False)
            # try:
            #     tool_learning_text+="\nThe exactly same image appears in the following web pages:\n"+visual_search(url, text)
            # except Exception as e:
            #     print("Error in visual search",e)

        else:
            tool_learning_text = None


        # image captioning
        if mode != 'direct' and mode != 'cot':
            print("Generating Image Captioning...")
            use_cache_flag = False
            if using_cache:
                if url in image_captioning_cache:
                    image_text = image_captioning_cache[url]
                    if 'sorry' not in image_text and 'Sorry' not in image_text:
                        use_cache_flag = True
                        print('Retrieved image caption result from cache')

            if not use_cache_flag:
                for i in range(max_retry):
                    try:
                        image_text = img2txt(url, data_name)
                        if 'sorry' in image_text.lower():
                            print('Image captioning error: LLM Failed, retrying...')
                            continue
                        break
                    except Exception as e:
                        print(f'Image caption error: {e}, retrying')
                else:
                    print('Image captioning error, skipping...')
                    continue
                if using_cache:
                    image_captioning_cache[url] = image_text
                    with open(image_caption_cache_name, 'w', encoding='utf-8') as f:
                        json.dump(image_captioning_cache, f)
        else:
            image_text = None

        if mode.startswith('lemma'):
            use_cache_flag = False

            if using_cache:
                if text in kg_cache:
                    kg = kg_cache[text]
                    kg1 = kg.split('---')[0]
                    kg2 = kg.split('---')[1]
                    kg3 = None
                    print('Retrieved KG result from cache')
                    use_cache_flag = True

            if not use_cache_flag:
                for i in range(max_retry):
                    try:
                        print('Generating KG...')
                        kg = kg_gen(text, image_text)
                        kg1 = kg.split('---')[0]
                        kg2 = kg.split('---')[1]
                        kg3 = None
                        break
                    except Exception as e:
                        print(f'KG error: {e}, retrying...')
                else:
                    print('KG error, skipping...')
                    continue

                if using_cache:
                    kg_cache[text] = kg
                    with open(kg_cache_name, 'w', encoding='utf-8') as f:
                        json.dump(kg_cache, f)

        # final prediction
        for i in range(max_retry):
            print('Final Prediction...')
            try:
                if mode == 'direct':
                    kg1, kg2, kg3, prob, explain = zero_shot(text, url, is_url=use_online_image)
                elif mode == 'cot':
                    kg1, kg2, kg3, prob, explain = cot(text, url, is_url=use_online_image)
                elif mode == 'cot+fact':
                    pass
                elif mode.startswith('lemma'):
                    prob, explain = lemma(text, url, tool_learning_text, kg1, kg2, zero_shot_pred, mode, zs_flag = zs_flag, is_url=use_online_image)
                else:
                    kg1, kg2, kg3, prob, explain = kg_generate_and_compare(text, image_text, tool_learning_text)
                break
            except Exception as e:
                print(f'Final prediction error: {e}, retrying...')
        else:
            print('Final prediction error, skipping...')
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
            print(
                'Result of index {}/{}: \nLabel: {}\nZero-shot: {}\nFinal: {}\nFinal Reasoning: {}'.format(len(labels),
                                                                                                            total_data_size,
                                                                                                            label,
                                                                                                            zero_shot_pred,
                                                                                                            pred_label,
                                                                                                            explain))

        with open(output_score, 'w', encoding='utf-8') as f:
            f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
        with open(output_result, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)

    evaluation_result = metric(labels, pred_labels)
    print('Evaluation result:', evaluation_result)
    write_metric_result(output_score, evaluation_result)

    if mode.startswith('lemma'):
        evaluation_result = metric(labels, zero_shot_labels)
        print('Zero-shot evaluation result:', evaluation_result)
        write_metric_result(output_score, evaluation_result, 'a', prefix='zero shot section')
