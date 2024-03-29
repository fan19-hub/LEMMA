

import replicate
import json
from configs import prompts_root,imgbed_root
from openai import OpenAI
client = OpenAI()

class InstructBLIP:
    def __init__(self,prompt, name, min_len=80, max_len=300,beam_size=5,len_penalty=1,repetition_penalty=3,top_p=0.9):
        with open(prompts_root + prompt, "r") as f:
            self.prompt_template = f.read()
        self.mode= "cot" if "cot" in prompt else "zero-shot"
        self.min_len=min_len,
        self.max_len=max_len,
        self.beam_size=beam_size,
        self.len_penalty=len_penalty,
        self.repetition_penalty=repetition_penalty,
        self.top_p=top_p

    def extra_post_process(self,output):
        max_tokens=1
        temperature=0.1
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": output},
                {"role": "system", "content": 'do user think the post contains misinformation? Your answer should be a single word from [yes, no].'}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        r=response.choices[0].message.content
        if "yes" in r:
            return "fake"
        elif "not" in r:
            return "real"
        else:
            return r

    def __call__(self, *args, **kwargs):
        image_path=""
        if 'image' in kwargs:
            image_path = kwargs['image']
            del kwargs['image']
        prompt = self.prompt_template.format(**kwargs)
        if 'http' not in image_path:
            image_path = imgbed_root + image_path
        input={
            "top_p": 0.9,
            "prompt": prompt,
            "max_len": 300,
            "min_len": 80,
            "beam_size": 5,
            "image_path": image_path,
            "len_penalty": 1,
            "repetition_penalty": 3
        }
        try:
            output = replicate.run(
                "gfodor/instructblip:ca869b56b2a3b1cdf591c353deb3fa1a94b9c35fde477ef6ca1d248af56f9c84",
                input=input
            ).lower()
        except:
            return None

        output_dict={}
        if self.mode=="cot":
            output_dict["label"]=self.extra_post_process(output)
            output_dict["explanation"]=output
            return output_dict
            
        for seg in output.split(" "):
            if "fake" in seg:
                output_dict["label"]="fake"
                break
            elif "real" in seg:
                output_dict["label"]="real"
                break
    
        if output_dict=={}:
            return None
        output_dict["explanation"]=output
        return output_dict





#=> "The man in the image appears to be expressing his emotio...






# from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
# import torch
# from PIL import Image
# import requests

# model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b")
# processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)
# url = "https://raw.githubusercontent.com/salesforce/LAVIS/main/docs/_static/Confusing-Pictures.jpg"
# image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
# prompt = "What is unusual about this image?"
# inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)

# outputs = model.generate(
#     **inputs,
#     do_sample=False,
#     num_beams=5,
#     max_length=256,
#     min_length=1,
#     top_p=0.9,
#     repetition_penalty=1.5,
#     length_penalty=1.0,
#     temperature=1,
# )
# generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
# print(generated_text)