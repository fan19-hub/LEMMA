import os
import openai


def run():
    prompt = open('prompt.md', 'r', encoding='utf-8')
    prompt_text = prompt.read()
    prompt.close()

    input_file = open('input', 'r', encoding='utf-8')
    input_text = input_file.read()
    input_file.close()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an expert in Knowledge Graph generation"},
            {"role": "user", "content": prompt_text + '\n' + input_text}
        ]
    )

    with open('output', 'w', encoding='utf-8') as f:
        f.write(completion.choices[0].message['content'])


if __name__ == '__main__':
    run()
