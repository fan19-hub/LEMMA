import json
import random
import time

import requests
from utils import stats
from toolLearning import text_search
from lemma_component import LemmaComponent

if __name__ == '__main__':
    data =      {
        "text": "I think that is an Angel ready to attack Central Dogma RT @World: Lenticular Clouds over Mount Fuji, Japan. http://t.co/y3Twrw5I0a",
        "image_url": "twitter/Mediaeval2016_TestSet_Images/fuji_lenticular_1.jpg",
        "tool_learning_text": 'Null',
        "label": 1,
        "prediction": 1,
        "explain": "The image shows a series of lenticular clouds over Mount Fuji, which are known to form in the troposphere typically in a perpendicular alignment to the wind direction. While the clouds can appear unusual and are often mistaken for UFOs or other phenomena, the text's reference to an 'Angel ready to attack Central Dogma' is a fictional scenario likely referencing the anime series 'Neon Genesis Evangelion' where beings called 'Angels' attack a location known as Central Dogma. This is not a real-world event, and the image is a natural meteorological occurrence, not an 'Angel.' Therefore, the text contains misinformation as it misrepresents a natural cloud formation as a fictional event.",
        "direct": 1,
        "direct_explain": "The image shows a series of lenticular clouds over Mount Fuji, which are known to form in the troposphere typically in a perpendicular alignment to the wind direction. While the clouds can appear unusual and are often mistaken for UFOs or other phenomena, the text's reference to an 'Angel ready to attack Central Dogma' is a fictional scenario likely referencing the anime series 'Neon Genesis Evangelion' where beings called 'Angels' attack a location known as Central Dogma. This is not a real-world event, and the image is a natural meteorological occurrence, not an 'Angel.' Therefore, the text contains misinformation as it misrepresents a natural cloud formation as a fictional event."
    }

    module_no_cap = LemmaComponent(prompt='kg_gen_no_cap_prompt.md', name='kg_gen2', model='gpt4v', using_cache=False,
                                   online_image=True, max_retry=3, max_tokens=1000, temperature=0.1)

    module_kg_comp = LemmaComponent(prompt='kg_comp_prompt_new.md', name='kg_comp', model='gpt4', using_cache=False,
                                    online_image=True, max_retry=3, max_tokens=1000, temperature=0.1)
    # temp = LemmaComponent(prompt='test.md', name='temp', model='gpt4v', using_cache=False,
    #                       online_image=True, max_retry=3, max_tokens=1000, temperature=0.1)

    result = module_no_cap(TEXT=data['text'], image=data['image_url'])
    print(result)
    result = module_kg_comp(KG=result)
    print(result)
    # result = temp(TEXT=data['text'], image=data['image_url'])
    # print(result)
