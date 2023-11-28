import os

import openai


def kg_generate_and_compare(text, image_text, kg_generate_prompt_path='kg_gen_prompt.md',
                            kg_compare_prompt_path='kg_comp_prompt.md'):
    with open(kg_generate_prompt_path, 'r', encoding='utf-8') as f:
        gen_prompt = f.read()
    with open(kg_compare_prompt_path, 'r', encoding='utf-8') as f:
        comp_prompt = f.read()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    print('Generating Text KG...')
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an expert in Knowledge Graph generation"},
            {"role": "user", "content": gen_prompt + '\n' + text + '\nKnowledge Graph Output:\n'}
        ]
    )
    text_kg = completion.choices[0].message['content']

    print('Generating Image KG...')
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an expert in Knowledge Graph generation"},
            {"role": "user", "content": gen_prompt + '\n' + image_text + '\nKnowledge Graph Output:\n'}
        ]
    )
    image_kg = completion.choices[0].message['content']

    print('Comparing...')
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an expert in Knowledge Graph comparison"},
            {"role": "user",
             "content": '{}\nfirst KG:\n{}\n{}\nSecond KG:\n{}\n{}\nYour Prediction:\n'.format(comp_prompt,
                                                                                               text,
                                                                                               text_kg,
                                                                                               image_text,
                                                                                               image_kg)}
        ],
        temperature=0.1,
    )
    return text_kg, image_kg, completion.choices[0].message['content']


if __name__ == '__main__':
    with open('text_input', 'r', encoding='utf-8') as f:
        text = f.read()
    with open('image_text_input', 'r', encoding='utf-8') as f:
        image_text = f.read()
    text_kg, image_kg, prediction = kg_generate_and_compare(text, image_text)
    print(prediction)
    with open('kg_final_output', 'w', encoding='utf-8') as f:
        f.write('Text KG:\n' + text_kg + '\n' + 'Image KG:\n' + image_kg + '\n' + 'Prediction:\n' + prediction)
