from config import prompts_root, imgbed_root
from utils import onlineImg_process, offlineImg_process

prompt_path = prompts_root + 'cot.md'
with open(prompt_path, 'r', encoding='utf-8') as f:
    prompt = f.read()


def cot(text, img_source, tool=None, is_url=True):
    global prompt
    if is_url:
        if "http" not in img_source:
            img_source = imgbed_root + img_source
        info = onlineImg_process(prompt.format(TEXT=text), img_source, max_tokens=300)
        info_list = info.split("\n")
        label = int(info_list[-1].strip())
        explanation = "\n".join(info_list[:-1])
    else:
        info = offlineImg_process(prompt.format(TEXT=text), img_source, max_tokens=300)
        info_list = info.split("\n")
        label = int(info_list[-1].strip())
        explanation = "\n".join(info_list[:-1])

    return None, None, None, label, explanation
