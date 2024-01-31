from config import prompts_root, imgbed_root

# Get the prompt
from utils import onlineImg_process, offlineImg_process

prompt_path = prompts_root + 'zero_shot.md'
with open(prompt_path, 'r', encoding='utf-8') as f:
    prompt = f.read()


def zero_shot(text, img_source, tool=None, is_url=True):
    global prompt
    if is_url:
        if "http" not in img_source:
            img_source = imgbed_root + img_source
        info = onlineImg_process(prompt.format(TEXT=text), img_source)
        info_list = info.split("\n")
        label = int(info_list[0].strip())
        explanation = "\n".join(info_list[1:])
    else:
        info = offlineImg_process(prompt.format(TEXT=text), img_source)
        info_list = info.split("\n")
        label = int(info_list[0].strip())
        explanation = "\n".join(info_list[1:])

    return None, None, None, label, explanation

    # completion = client.chat.completions.create(
    #     model="gpt-4-vision-preview",
    #     messages=[
    #         {"role": "system",
    #          "content": "You are an expert in Misinformation Detection"},
    #         {"role": "user",
    #          "content": prompt.format(TEXT=text, IMAGE=image_url)}
    #     ],
    #     temperature=0.1,
    # )
    # predicted_label = int(completion.choices[0].message.content.split('\n')[0].strip())
    # return None, None, None, predicted_label, completion.choices[0].message.content
