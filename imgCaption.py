import os
import base64
import requests
import openai
from openai import OpenAI
from config import data_root, prompts_root, imgbed_root

# Openai settings
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Get the prompt
with open(prompts_root+"img_caption.md","r") as f:
    prompt=f.read()

def onlineImg_process(url):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
          {
            "role": "user",
            "content": [
              {"type": "text", "text": prompt},
              {
                "type": "image_url",
                "image_url": {
                  "url": f"{url}",
                },
              },
            ],
          }
        ],
        max_tokens=300,
        temperature=0.1
      )
    return response.choices[0].message.content


def offlineImg_process(image_path):
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
      "max_tokens": 300,
      "temperature":0.1
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return eval(response.text)["choices"][0]["message"]["content"]



def img2txt(source= data_root+"weibo", is_url=True):
  global prompt
  print("Generating Image Captioning...")
  if is_url:
    if "http" not in source: 
      source=imgbed_root+source
    return onlineImg_process(source) 
  else:
      return offlineImg_process(source)


