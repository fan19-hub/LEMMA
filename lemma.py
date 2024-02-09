from config import prompts_root, imgbed_root
from utils import onlineImg_process, offlineImg_process

def reason_modify(text, url, definition, q1, q2, tool, original_reason, is_url=True):
    CATEGORY = ["True", "Satire/Parody", "Misleading Content", "Imposter Content", "False Connection", "Manipulated Content", "Unverified"]
    reason_modify_prompt_path = prompts_root + 'reason_modify.md'
    with open(reason_modify_prompt_path, 'r', encoding='utf-8') as f:
        reason_modify_prompt = f.read()

    if is_url:
        if "http" not in url:
            url = imgbed_root + url
        info = onlineImg_process(reason_modify_prompt.format(TEXT=text,
                                                    ORIGINAL_REASONING=original_reason,
                                                    Question1 = q1,
                                                    Question2 = q2,
                                                    TOOLLEARNING=tool,
                                                    DEFINITION = definition), url, max_tokens=1000)
    else:
        info = offlineImg_process(reason_modify_prompt.format(TEXT=text,
                                                    ORIGINAL_REASONING=original_reason,
                                                    Question1 = q1,
                                                    Question2 = q2,
                                                    TOOLLEARNING=tool,
                                                    DEFINITION = definition), url, max_tokens=1000)
    print(info)
    text = info.split("\n")[-1]

    for category in CATEGORY:
        if category.lower() in text.lower():
            if category == "True":
                pred = 0
            elif category == "Unverified":
                pred = None
            else:
                pred = 1
            
    return pred

def lemma(text, url, tool, kg1, kg2, pred_label, intuition, method, zs_flag, is_url=True):
    if zs_flag == True:
        lemma_prompt_path = prompts_root + method + '_true.md'
    else:
        lemma_prompt_path = prompts_root + method + '_false.md'

    with open(lemma_prompt_path, 'r', encoding='utf-8') as f:
        lemma_prompt = f.read()

    if intuition:
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
    else: 
        if is_url:
            if "http" not in url:
                url = imgbed_root + url
            info = onlineImg_process(lemma_prompt.format(TEXT=text,
                                                        TEXT_KG=kg1,
                                                        IMAGE_KG=kg2,
                                                        TOOLLEARNING=tool), url, max_tokens=1000)
        else:
            info = offlineImg_process(lemma_prompt.format(TEXT=text,
                                                        TEXT_KG=kg1,
                                                        IMAGE_KG=kg2,
                                                        TOOLLEARNING=tool), url, max_tokens=1000)
            

    info_list = info.split("\n")
    final_label = int(info_list[-1].strip())
    explanation = "\n".join(info_list[:-1])
    return final_label, explanation
