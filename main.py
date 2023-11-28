import os


import json
from imgCaption import img2txt
from kg_generate_and_compare import kg_generate_and_compare



if __name__ == '__main__':
    # Open the JSON file
    with open('exampleinput.json') as file:
        data = json.load(file)

    results=[]
    labels=[]
    view=False
    for item in data:
        # read
        url   = item["image_url"]
        text  = item["original_post"]
        label = item["label"]
        # image captioning
        image_text = img2txt(url)
        # KG generation and compare
        text_kg, image_kg, prediction = kg_generate_and_compare(text, image_text)
        results.append(prediction)
        labels.append(label)
        if view:
            print(prediction)
            with open('kg_final_output', 'w', encoding='utf-8') as f:
                f.write('Text KG:\n' + text_kg + '\n' + 'Image KG:\n' + image_kg + '\n' + 'Prediction:\n' + prediction)
   
    
   