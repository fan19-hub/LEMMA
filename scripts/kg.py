from config import prompts_root
from openai import OpenAI


def kg_gen(text, image_text):
    client = OpenAI()

    kg_generate_prompt_path = prompts_root + 'kg_gen_prompt.md'

    with open(kg_generate_prompt_path, 'r', encoding='utf-8') as f:
        gen_prompt = f.read()

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an expert in Knowledge Graph generation"},
            {"role": "user",
             "content": gen_prompt.format(TEXT=text, IMAGETEXT=image_text, TOOL='No third text. Please ignore.')}
        ]
    )
    kg = completion.choices[0].message.content

    return kg
