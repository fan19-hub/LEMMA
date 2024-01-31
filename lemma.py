from config import prompts_root, imgbed_root
from utils import onlineImg_process, offlineImg_process


def lemma(text, url, tool, kg1, kg2, pred_label, method, is_url=True):
    lemma_prompt_path = prompts_root + method + '.md'

    with open(lemma_prompt_path, 'r', encoding='utf-8') as f:
        lemma_prompt = f.read()

    if is_url:
        if "http" not in url:
            url = imgbed_root + url
        info = onlineImg_process(lemma_prompt.format(TEXT=text,
                                                     PREDICTION=pred_label,
                                                     TEXT_KG=kg1,
                                                     IMAGE_KG=kg2,
                                                     TOOLLEARNING=tool), url, max_tokens=1000)
    else:
        info = offlineImg_process(lemma_prompt.format(TEXT=text,
                                                      PREDICTION=pred_label,
                                                      TEXT_KG=kg1,
                                                      IMAGE_KG=kg2,
                                                      TOOLLEARNING=tool), url, max_tokens=1000)

    info_list = info.split("\n")
    final_label = int(info_list[-1].strip())
    explanation = "\n".join(info_list[:-1])
    return final_label, explanation
