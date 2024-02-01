from config import prompts_root, imgbed_root
from utils import onlineImg_process, offlineImg_process
import json

# Get the prompt
prompt_path = prompts_root + 'zero_shot.md'
with open(prompt_path, 'r', encoding='utf-8') as f:
    prompt = f.read()


def zero_shot(text, img_source, tool=None, is_url=True):
    global prompt
    if is_url:
        if "http" not in img_source:
            img_source = imgbed_root + img_source
        info = onlineImg_process(prompt.format(TEXT=text), img_source)
        
    else:
        info = offlineImg_process(prompt.format(TEXT=text), img_source)
    info_dict=json.loads(info)
    label=info_dict['label']
    if label not in [0,1]:
        if label in ["0","1"]:
            label = int(label)
        else:
            raise ValueError("The label is not 0 or 1")
    explanation = info_dict['explanation']
    return None, None, None, label, explanation


# if __name__=="__main__":
#     print(zero_shot("Boston Marathon Bombing 'news' actor identified again! This man is an American soldier who lost his legs in Afghanistan. Live video may be arranged by the cameraman shot, the so-called bomb is only a smoke bomb, the damage to people is extremely limited, barely produced a smoke effect. @Beijing Youth Daily @New Weekly @Rui Chenggang @Huang Jianxiang @Internet forefront @Grotesque psychological behavior", "weibo/rumor_images/3b9c937bjw1e3rs645jowj.jpg",is_url= True))
