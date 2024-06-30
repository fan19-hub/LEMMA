import os
import json
from lemma_component import LemmaComponent
from retrieval import get_evidence, visual_search, driver_quit
from configs import out_root, definition_path
from utils import save, process_multilines_output, perror
import traceback

# Config
resume = True
using_cache = False
data_name = 'twitter'
start_index, end_index = 0, 1000


# Input file name
if data_name == 'twitter':
    input_file = "data/twitter/twitter.json"
    use_online_image = True
elif data_name == 'fakeddit':
    input_file = "data/fakeddit/FAKEDDIT.json"
    use_online_image = True
elif data_name == 'example':
    input_file = "data/example_input.json"
    use_online_image = True
else:
    raise ValueError('Invalid data name')

with open(input_file, encoding='utf-8') as f:
    data = json.load(f)


# Output file names
output_score = out_root + "lemma_" + data_name + "_score"
output_result = out_root + "lemma_" + data_name + "_output.json"
if not os.path.exists(out_root):
    os.makedirs(out_root)   

# Resume
labels = []
direct_labels = []
final_preds = []
total_data_size = len(data)
current_index = -1
logger = []
if resume and os.path.exists(output_score):
    with open(output_score, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        labels = []
        for char in lines[1]:
            if char.isdigit():
                labels.append(int(char))
        direct_labels = []
        for char in lines[3]:
            if char.isdigit():
                direct_labels.append(int(char))
        final_preds = []
        for char in lines[5]:
            if char.isdigit():
                final_preds.append(int(char))
        current_index = int(lines[6].split(':')[1].strip())
    with open(output_result, 'r', encoding='utf-8') as f:
        logger = json.load(f)
    total_data_size = len(data)
    data = data[current_index + 1:]
if current_index==-1:
    print('Starting from index 0')
else:
    print('Resuming from index:', current_index, ', Next index:', current_index + 1)


# LEMMA Components Initialization
direct_module = LemmaComponent(prompt='lemma_direct.md', name='Direct', 
                                model='gpt4v', using_cache=using_cache,
                                  online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                  post_process=lambda x: json.loads(x))
external_knowledge_module = LemmaComponent(prompt='external_knowledge.md', name='external_knowledge',       
                                  model='gpt4v', using_cache=using_cache,
                                  online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                  post_process=lambda x: json.loads(x))
question_gen_module = LemmaComponent(prompt='question_gen.md', name='question_gen', 
                                     model='gpt4v', using_cache=using_cache,
                                     online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                     post_process=lambda x: json.loads(x))
refine_prediction_module = LemmaComponent(prompt='refined_prediction.md', name='modify_reasoning', 
                                          model='gpt4v',using_cache=False,
                                         online_image=use_online_image, max_retry=3, max_tokens=1000, temperature=0.1,
                                         post_process=process_multilines_output)

# Test
for i, item in enumerate(data):
    current_index += 1
    if current_index<start_index:
        continue
    elif current_index>end_index:
        break
    print('Processing index {}/{}'.format(current_index, total_data_size))

    # Get input data
    url = item["image_url"]
    text = item["original_post"]
    label = item["label"]

    # Direct Prediction
    direct = direct_module(TEXT=text, image=url)
    print(direct)
    
    if direct is None: continue
    direct_pred = 0 if "real" in direct['label'].lower() else 1
    direct_explain = direct['explanation']

    # External Knowledge
    # Decide whether external knowledge is needed to further examine the input sample
    decision_external = external_knowledge_module(REASONING = direct_explain, TEXT = text, image=url)
    direct_external = 0 if "no" in decision_external['external knowledge'].lower() else 1 
    print("######################")
    print("Need External Knowledge:", direct_external)
    print(decision_external['explanation'])
    print("######################")

    retrieved_text = None
    if direct_external == 1:
        # Query Generation
        question_gen = question_gen_module(TEXT=text, 
                                            PREDICTION=direct_pred, 
                                            REASONING=direct_explain,
                                            image=url)
        
        if question_gen is None: continue
        title, questions = question_gen['title'], question_gen['questions']

        # Evidence Retrieval
        print("Lemma Component Evidence Retrieval: Starting...")
        try:
            retrieved_text = get_evidence(text, title, questions)
        except Exception as e:
            perror(traceback.format_exc())
            retrieved_text = ""

        try:
            visual_retrieved_text = visual_search(url, text)
        except Exception as e:
            perror(traceback.format_exc())
            visual_retrieved_text = ""

        # Refined Prediction
        rumor_types=["true", "satire/parody", "misleading content", "text image contradiction", "manipulated content", "unverified"]
        refine_result = refine_prediction_module(TEXT=text,
                                               ORIGINAL_REASONING=direct_explain,
                                               EXTERNAL=retrieved_text,
                                               EXTERNAL_VISUAL=visual_retrieved_text,
                                               DEFINITION=open(definition_path, 'r').read(),
                                               image=url)
        
        # Result Postprocessing
        if refine_result is None: continue
        refined_pred = refine_result["label"]
        refined_explain =  refine_result

        for rumor_type in rumor_types:
            if rumor_type.lower() in refined_pred.lower():
                refined_pred = rumor_type
                break  
        if refined_pred == 'true':
            final_pred = 0
        elif refined_pred == 'unverified':
            final_pred = direct_pred   # If model is not sure, go back to direct prediction
        else:
            final_pred = 1
        print('Refined Prediction:', refined_pred)
        final_explain = refined_explain
        retrieved_text = retrieved_text + visual_retrieved_text

    else:
        final_pred = direct_pred
        final_explain = direct_explain

    # Logging
    labels.append(label)
    direct_labels.append(direct_pred)
    final_preds.append(final_pred)
    logger.append({
        'text': text,
        'image_url': url,
        'tool_learning_text': retrieved_text,
        'label': label,
        'prediction': final_pred,
        'explain': final_explain,
        'direct': direct_pred,
        'direct_explain': direct_explain,
    })

    print('\nLabel:', label, ', Refined Prediction:', final_pred, ', Direct:', direct_pred)
    print('Refined Explain:', final_explain)

    save(labels, final_preds, direct_labels, current_index, logger, output_result, output_score)
    
driver_quit()