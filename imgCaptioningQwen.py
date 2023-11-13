
import re
from http import HTTPStatus
import dashscope
import os
 


def getImgDescript(imgUrl):
    imgUrl="https://z1.ax1x.com/2023/11/11/pi8DM6A.jpg"
    messages = [
        {
            "role": "user",
            "content": [
                {"image": imgUrl},
                {"text": "Let's think step by step. First, extract all the text in the image (OCR). Then, describe this picture. If it is a photo, how many characters are in this pic? what are they doing? what are their relations. what is the background? what activity is this? If it is a chart, what kind of chart it is? what interesting data does it have? what is the title or purpose of this chart? use 200 words to answer"}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model=dashscope.MultiModalConversation.Models.qwen_vl_chat_v1,
                                                     messages=messages)
    
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0]["message"]["content"]
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.
        return -1
   

def imgtagProcess(match):
    #get the url of the image
    rawUrl=match.group(1)
    match2=re.match(r".*?(\.jpg|\.png|\.webp|\.jpeg)",rawUrl)
    if match2==-1:
        return -1
    imgUrl=match2.group()

    #get the image caption
    captionHeader = "Here is the description of a relevant image."
    captionEnded = "Here is the end of the image description."
    imgDescript = getImgDescript(imgUrl)
    if imgDescript==-1:
        return match.group()
    else:
        return captionHeader + imgDescript + captionEnded
    

def replaceImg(content):
    # Image tag pattern: ![alt text](image_url)
    replaced_content = re.sub(r'!\[.*?\]\((.*?)\)', imgtagProcess , content)
    # Printing the found image tags
    print(replaced_content)


# os.popen("$env:DASHSCOPE_API_KEY = 'sk-fb8883fe0da04d81ba3392724e5f5a7f'")

replaceImg('''
![](https://www.freeimg.cn/i/2023/11/11/654ebb6059547.jpg)
'''
)



# import requests
# import base64
# def img2url(filename,YourClientID='b69c55c08466d2e'):
#     # 读取本地图片文件
#     with open(filename, 'rb') as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

#     # 设置请求头和参数
#     headers = {'Authorization': f'Client-ID {YourClientID}'}
#     payload = {'image': encoded_string}

#     # 发送POST请求
#     response = requests.post('https://api.imgur.com/3/image', headers=headers, data=payload)

#     # 获取上传后的图片链接
#     if response.status_code == 200:
#         return response.json()['data']['link']
#     else:
#         print('上传图片失败')
#         return -1






