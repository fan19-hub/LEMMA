import base64
import os
import requests

from zero_shot import zero_shot
from config import prompts_root
from openai import OpenAI


def lemma(text, url, image_text, tool):
    _, _, _, prob, _ = zero_shot(text, url)
    pred_label = int(prob)

    client = OpenAI()

    kg_generate_prompt_path = prompts_root + 'kg_gen_prompt.md'
    lemma_prompt_path = prompts_root + 'lemma.md'

    with open(kg_generate_prompt_path, 'r', encoding='utf-8') as f:
        gen_prompt = f.read()

    with open(lemma_prompt_path, 'r', encoding='utf-8') as f:
        lemma_prompt = f.read()

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an expert in Knowledge Graph generation"},
            {"role": "user",
             "content": gen_prompt.format(TEXT=text, IMAGETEXT=image_text, TOOL='No third text. Please ignore.')}
        ]
    )

    kg = completion.choices[0].message.content
    kg1 = kg.split('---')[0]
    kg2 = kg.split('---')[1]

    if 'http' in url:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "user",
                 "content": [
                     {"type": "text", "text": lemma_prompt.format(TEXT=text,
                                                                  PREDICTION=pred_label,
                                                                  TEXT_KG=kg1,
                                                                  IMAGE_KG=kg2,
                                                                  TOOLLEARNING=tool)},
                     {"type": "image_url", "image_url": {"url": f"{url}", }, },
                 ],
                 }
            ],
            max_tokens=300,
            temperature=0.1
        )
        info = response.choices[0].message.content

    else:
        # Encode function
        api_key = os.getenv("OPENAI_API_KEY")

        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        # Getting the base64 string
        base64_image = encode_image(url)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": lemma_prompt.format(TEXT=text,
                                                        PREDICTION=pred_label,
                                                        TEXT_KG=kg1,
                                                        IMAGE_KG=kg2,
                                                        TOOLLEARNING=tool)
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300,
            "temperature": 0.1
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        info = eval(response.text)["choices"][0]["message"]["content"]

    info_list = info.split("\n")
    final_label = int(info_list[-1].strip())
    explanation = "\n".join(info_list[:-1])
    print(pred_label, final_label, explanation)
    return kg1, kg2, None, final_label, explanation
