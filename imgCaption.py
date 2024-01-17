import os
import openai
from openai import OpenAI
import base64
import requests
openai.api_key = os.getenv("OPENAI_API_KEY")
from config import data_root, prompts_root



client = OpenAI()
with open(prompts_root+"img_caption.md","r") as f:
    prompt=f.read()


def img2txt(url, data_name=data_root+"weibo"):
  global prompt
  print("Generating Image Captioning...")

  if "http" in url:
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
      )
      return response.choices[0].message.content
  else:
      # OpenAI API Key
      api_key = os.getenv("OPENAI_API_KEY")

      # Function to encode the image
      def encode_image(image_path):
        if data_name == "weibo":
          rumor_img_dir = "../nlp-project/Data/weibo/nonrumor_images/"
          rumor_img_dir = os.path.abspath(rumor_img_dir)

          non_rumor_img_dir = "../nlp-project/Data/weibo/rumor_images/"
          non_rumor_img_dir = os.path.abspath(non_rumor_img_dir)       

          for filename in os.listdir(rumor_img_dir):
            if filename == image_path:
              image_path = rumor_img_dir + "/" + image_path
              break

          for filename in os.listdir(non_rumor_img_dir): 
            if filename == image_path:
              image_path = non_rumor_img_dir + "/" + image_path
              break  
          
          with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
          
        elif data_name == "twitter":
          img_dir = "../nlp-project/Data/twitter/Mediaeval2016_TestSet_Images"

          for filename in os.listdir(img_dir):
            if filename[:-4] == image_path:
              image_path = img_dir + "/" + image_path + ".jpg"
              break

          with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


      # Path to your image
      image_path = url

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
        "max_tokens": 300
      }

      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

      return eval(response.text)["choices"][0]["message"]["content"]


