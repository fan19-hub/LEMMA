import json
from config import prompts_root, imgbed_root

# Get the prompt
from utils import onlineImg_process, offlineImg_process

prompt_path = prompts_root + 'question_gen.md'
with open(prompt_path, 'r', encoding='utf-8') as f:
    prompt = f.read()


def question_gen(text, img_source, zero_shot_pred, is_url=True):
    global prompt
    if is_url:
        if "http" not in img_source:
            img_source = imgbed_root + img_source
        questions = json.loads(onlineImg_process(prompt.format(TEXT=text, PREDICTION=zero_shot_pred), img_source))
    else:
        questions = json.loads(offlineImg_process(prompt.format(TEXT=text, PREDICTION=zero_shot_pred), img_source))
    return questions
