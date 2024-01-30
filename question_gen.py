import json
import os
import openai
from openai import OpenAI
from config import prompts_root, imgbed_root

# Openai settings
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Get the prompt
prompt_path = prompts_root + 'question_gen.md'
with open(prompt_path, 'r', encoding='utf-8') as f:
    prompt = f.read()


def onlineImg_process(url, text, zero_shot_pred):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user",
             "content": [
                 {"type": "text", "text": prompt.format(TEXT=text, PREDICTION=zero_shot_pred)},
                 {"type": "image_url", "image_url": {"url": f"{url}", }, },
             ],
             }
        ],
        max_tokens=1000,
        temperature=0.1
    )
    info = response.choices[0].message.content
    return json.loads(info)


def question_gen(text, img_source, zero_shot_pred):
    global prompt
    if "http" not in img_source:
        img_source = imgbed_root + img_source
    questions = onlineImg_process(img_source, text, zero_shot_pred)
    return questions
