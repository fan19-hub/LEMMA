import os
import openai
import base64
import requests
from openai import OpenAI
from config import prompts_root,imgbed_root

# Openai settings
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Get the prompt
prompt_path=prompts_root+'zero_shot.md'
with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt = f.read()


def onlineImg_process(url, text):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
                {"role": "user",
                    "content": [
                    {"type": "text", "text": prompt.format(TEXT=text)},
                    {"type": "image_url", "image_url": {"url": f"{url}",},},
                    ],
                }
                ],
        max_tokens=1000,
        temperature=0.1
    )
    info=response.choices[0].message.content
    info_list=info.split("\n")
    label=int(info_list[0].strip())
    explanation="\n".join(info_list[1:])
    return label,explanation


def offlineImg_process(image_path,text):
    # OpenAI API Key
    api_key = os.getenv("OPENAI_API_KEY")

    # Encode function
    def encode_image(image_path):
      with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
      
    # Getting the base64 string
    base64_image = encode_image(image_path)

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
              "text": prompt
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
      "max_tokens": 1000,
      "temperature":0.1
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    info= eval(response.text)["choices"][0]["message"]["content"]
    info_list=info.split("\n")
    label=int(info_list[0].strip())
    explanation="\n".join(info_list[1:])
    
    return label,explanation


def zero_shot(text, img_source, tool=None,is_url=True,):
    global prompt
    print('Predicting...')
    if is_url:
        if "http" not in img_source: 
            img_source=imgbed_root+img_source
        print(img_source)
        label, explanation=onlineImg_process(img_source,text) 
    else:
        print(img_source)
        label, explanation= offlineImg_process(img_source,text)
    print(label, explanation)

    return None, None, None, label, explanation











    # completion = client.chat.completions.create(
    #     model="gpt-4-vision-preview",
    #     messages=[
    #         {"role": "system",
    #          "content": "You are an expert in Misinformation Detection"},
    #         {"role": "user",
    #          "content": prompt.format(TEXT=text, IMAGE=image_url)}
    #     ],
    #     temperature=0.1,
    # )
    # predicted_label = int(completion.choices[0].message.content.split('\n')[0].strip())
    # return None, None, None, predicted_label, completion.choices[0].message.content

