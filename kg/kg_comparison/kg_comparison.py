import os

import openai


def run():
    prompt = open('prompt.md', 'r', encoding='utf-8')
    prompt_text = prompt.read()
    prompt.close()

    input_file1 = open('text_kg', 'r', encoding='utf-8')
    input_text1 = input_file1.read()
    input_file1.close()

    input_file2 = open('image_kg', 'r', encoding='utf-8')
    input_text2 = input_file2.read()
    input_file2.close()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an expert in Knowledge Graph comparison"},
            {"role": "user",
             "content": prompt_text + '\n' + 'first KG:\n' + input_text1 + '\nSecond KG:\n' + input_text2 + '\nYour Prediction:\n'}
        ],
        temperature=0.1,
    )

    with open('output', 'w', encoding='utf-8') as f:
        f.write(completion.choices[0].message['content'])


if __name__ == '__main__':
    run()
