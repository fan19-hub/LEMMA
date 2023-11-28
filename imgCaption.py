from openai import OpenAI
import openai
from config import OPENAI_KEY
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPENAI_KEY

client = OpenAI()

def img2txt(url):
  print("Generating Image Captioning...")
  if "http:" in url:
      response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
          {
            "role": "user",
            "content": [
              {"type": "text", "text": "Let's think step by step. First, extract all the text in the image (OCR). Then, describe this picture. If it is a photo, how many characters are in this pic? what are they doing? what are their relations. what is the background? what activity is this? If it is a chart, what kind of chart it is? what interesting data does it have? what is the title or purpose of this chart? use 200 words to answer"},
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
      import base64
      import requests

      # OpenAI API Key
      # api_key = OPENAI_KEY
      api_key = os.getenv("OPENAI_API_KEY")

      # Function to encode the image
      def encode_image(image_path):
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
                "text": "Let's think step by step. First, extract all the text in the image (OCR). Then, describe this picture. If it is a photo, how many characters are in this pic? what are they doing? what are their relations. what is the background? what activity is this? If it is a chart, what kind of chart it is? what interesting data does it have? what is the title or purpose of this chart? use 200 words to answer"
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


