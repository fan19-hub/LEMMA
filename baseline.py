import json
from lemma_component import LemmaComponent
from toolLearning import evidence_retreival
from config import data_root, out_root, definition_path
from utils import save, save_baseline, process_multilines_output, image_caption

# mode ('direct' or 'cot' or 'cot+kg' or 'cot+fact' or 'lemma')
#### EXPLANATION ####
# direct: directly use the text and image as input
# cot: use chain of thought method
# cot+kg: use chain of thought method and knowledge graph based reasoning
# cot+fact: use chain of thought method and fact check
# lemma: our method
mode = 'zero-shot'
model = "gpt3.5"

# print the result
view = True

# automatic resume
resume = False

# zero-shot conditional result
zs_flag = True

# intuition
intuition = True

# dataset (twitter or weibo or fakereddit or ticnn)
data_name = 'twitter'

# input data file name
if data_name == 'twitter':
    input_file = data_root + 'twitter/twitter_shuffled.json'
    use_online_image = True
elif data_name == 'weibo':
    input_file = data_root + 'weibo/weibo_50_2.json'
    use_online_image = False
elif data_name == 'fakereddit':
    input_file = data_root + 'fakereddit/FAKEDDIT_shuffled.json'
    use_online_image = True
elif data_name == 'ticnn':
    input_file = data_root + 'ticnn/ticnn_sample.json'
    use_online_image = True
elif data_name == 'fakehealth':
    input_file = data_root + 'fakehealth/fakehealth.json'
    use_online_image = True
elif data_name == 'weibo21':
    input_file = data_root + 'weibo21/weibo21_shuffle_1.json'
    use_online_image = False
elif data_name == 'pheme':
    input_file = data_root + 'PHEME/PHEME_reshuffled.json'
    use_online_image = True
elif data_name == 'test':
    input_file = data_root + 'exampleinput.json'
    use_online_image = True
else:
    raise ValueError('Invalid data name')

# output file names
output_score = out_root + data_name + '_' + mode + '_' + model + '_' + 'result'
output_result = out_root + data_name + '_' + mode + '_' + model + '_' + 'output.json'
with open(input_file, encoding='utf-8') as file:
    data = json.load(file)


if resume:
    with open(output_score, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        labels = []
        for char in lines[1]:
            if char.isdigit():
                labels.append(int(char))
        zero_shot_labels = []
        for char in lines[3]:
            if char.isdigit():
                zero_shot_labels.append(int(char))
        pred_labels = []
        for char in lines[5]:
            if char.isdigit():
                pred_labels.append(int(char))
        current_index = int(lines[6].split(':')[1].strip())
    with open(output_result, 'r', encoding='utf-8') as f:
        all_results = json.load(f)
    total_data_size = len(data)
    data = data[current_index + 1:]
    print('Resuming from index:', current_index, ', Next index:', current_index + 1)
else:
    pred_labels = []
    labels = []
    zero_shot_labels = []
    total_data_size = len(data)
    print('Starting from index 0')
    current_index = -1
    all_results = []


if model=="gpt4v":
    if mode=="zero-shot":
        baseline_module = LemmaComponent(prompt='zero_shot.md', name='zero_shot', model=model, using_cache=True,
                                        online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                        post_process=lambda x: json.loads(x))                       
    elif mode=="cot":
        baseline_module = LemmaComponent(prompt='cot.md', name='cot', model=model, using_cache=True,
                online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                post_process=process_multilines_output)
    else:
        raise Exception(f"Invalid mode: {mode}")

    
elif model=="gpt3.5":
    if mode=="zero-shot":
        baseline_module = LemmaComponent(prompt='zero_shot_gpt35.md', name='zero-shot_gpt35', model=model, using_cache=True,
                online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                post_process=process_multilines_output)
    elif mode=="cot":
        baseline_module = LemmaComponent(prompt='cot_gpt35.md', name='cot_gpt35', model=model, using_cache=True,
                online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                post_process=process_multilines_output)
    else:
        raise Exception(f"Invalid mode: {mode}")
else:
    raise Exception(f"Invalid Language model: {model}")



for i, item in enumerate(data):
    current_index += 1
    if current_index>200:
        break
    print('Processing index {}/{}'.format(current_index, total_data_size))

    # Get input data
    url = item["image_url"]
    text = item["original_post"]
    label = item["label"]

    # Direct prediction        
    if model in ["gpt3.5","gpt4"]:
        caption =  image_caption(url)
        if caption=="": continue
        response = baseline_module(TEXT=text, CAPTION=caption, image=url)
    else:
        response = baseline_module(TEXT=text, image=url)
    if response is None:
        continue
    prediction = 0 if "real" in response['label'].lower() else 1
    explanation = response['explanation']


    print("######################WHY")
    print('Label:', label, ', Prediction:', prediction)
    if mode=="cot":
        print("Reasoning:", explanation)
    print("######################")


    tool_learning_text = None
    pred_labels.append(prediction)
    labels.append(label)

    all_results.append({
        'text': text,
        'image_url': url,
        'label': label,
        'prediction': prediction,
        'explain': explanation,
    })

    save_baseline(labels, pred_labels, current_index, all_results, output_result, output_score)

    
