import json
from lemma_component import LemmaComponent
from toolLearning import text_search
from config import data_root, out_root, definition_path
from utils import save

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

# intuition
intuition = True

# dataset (twitter or weibo or fakereddit or ticnn)
data_name = 'twitter'

# input data file name
if data_name == 'twitter':
    input_file = data_root + 'twitter/wrong1to0.json'
    use_online_image = True
elif data_name == 'weibo':
    input_file = data_root + 'weibo/weibo.json'
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
    input_file = data_root + 'weibo21/weibo21.json'
    use_online_image = False
else:
    raise ValueError('Invalid data name')

# output file names
output_score = out_root + data_name + '_' + mode + '_' + 'result'
output_result = out_root + data_name + '_' + mode + '_' + 'kg_final_output.json'

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
    with open(output_score, 'w', encoding='utf-8') as f:
        f.write('Labels:\n{}\nPredictions:\n{}\n'.format(labels, pred_labels))
    with open(output_result, 'w', encoding='utf-8') as f:
        f.write('')
    current_index = -1
    all_results = []

zero_shot_module = LemmaComponent(prompt='zero_shot_question_gen.md', name='zero_shot', model='gpt4v', using_cache=True,
                                  online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                  post_process=lambda x: json.loads(x))
modify_reasoning_module = LemmaComponent(prompt='reason_modify.md', name='modify_reasoning', model='gpt4v', using_cache=True,
                                         online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                         post_process=lambda x: (x.split('\n')[-1], x))

for i, item in enumerate(data):
    current_index += 1
    print('Processing index {}/{}'.format(current_index, total_data_size))
    url = item["image_url"]
    text = item["original_post"]
    label = item["label"]

    zero_shot = zero_shot_module(TEXT=text, image=url)
    zero_shot_label = zero_shot['label']
    zero_shot_explain = zero_shot['explanation']
    zero_shot_title = zero_shot['title']
    zero_shot_questions = zero_shot['questions']
    zero_shot_external = zero_shot['external knowledge']

    if zero_shot_external == 1:
        
        tool_learning_text = text_search(zero_shot_title)
        for q in zero_shot_questions:
            tool_learning_text += text_search(q)

        modified_label, modified_reasoning = modify_reasoning_module(TEXT=text,
                                                                    ORIGINAL_REASONING=zero_shot_explain,
                                                                    Question1=zero_shot_questions[0],
                                                                    Question2=zero_shot_questions[1],
                                                                    TOOLLEARNING=tool_learning_text,
                                                                    DEFINITION=open(definition_path, 'r').read(),
                                                                    image=url)

        if modified_label == 'True':
            pred_label = 0
        elif modified_label == 'Unverified':
            pred_label = zero_shot_label
        else:
            pred_label = 1

    pred_labels.append(pred_label)
    labels.append(label)
    zero_shot_labels.append(zero_shot_label)

    all_results.append({
        'text': text,
        'image_url': url,
        'tool_learning_text': tool_learning_text,
        'label': label,
        'prediction': pred_label,
        'explain': modified_reasoning,
        'direct': zero_shot_label,
        'direct_explain': zero_shot_explain,
    })

    save(labels, pred_labels, zero_shot_labels, current_index, all_results, output_result, output_score)

if __name__ == '__main__':
    pass
