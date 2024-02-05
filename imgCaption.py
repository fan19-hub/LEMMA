from config import data_root, prompts_root, imgbed_root

# Openai settings
from utils import onlineImg_process, offlineImg_process


# Get the prompt
with open(prompts_root + "img_caption.md", "r") as f:
    prompt = f.read()


def img2txt(source=data_root + "weibo", is_url=True):
    global prompt
    if is_url:
        if "http" not in source:
            source = imgbed_root + source
        return onlineImg_process(prompt, source, max_tokens=1000)
    else:
        return offlineImg_process(prompt, source, max_tokens=1000)
if __name__ == "__main__":
    print(img2txt(source= "weibo/rumor_images/476b66c1jw1dwnz5den2cj.jpg", is_url=True))
