
import json
import os
from PIL import Image
from openai import OpenAI

    

# # Set up OpenAI API
# client=OpenAI()
# # Define a function to generate questions using GPT-3.5
# def generate_questions(prompt):
#     completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         # model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system",
#              "content": "You are an professional in text cleaning and main body extraction"},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     response = completion.choices[0].message.content
#     return response


# 1. 把图片格式转换为jpg
files = os.listdir(".")
# Traverse through each file
for file in files:
    ext=file.split(".")[-1]
    if ext=="jpg" or ext=="py" or ext=="json":
        continue
    image = Image.open(file)
    
    # Change the format to JPG
    # Convert RGBA to RGB if necessary
    if image.mode == "RGBA":
        image = image.convert("RGB")
    new_path = os.path.splitext(file)[0] + ".jpg"
    image.save(new_path, "JPEG")
    os.remove(file)


# # 2. 把json文件中不符合要去的数据去掉
# #change it!
# with open("1.json","r") as f:
#     data=json.load(f)
# new_data={}
# for item in data:
#     if item["img_url"]=="21_0":
#         pass
#     if len(item["post_text"])<8000 and len(item["post_text"])>1000 and "Page" not in item["post_text"] and "access denied" not in item["post_text"].lower() and "not found" not in item["post_text"].lower() and "forbidden" not in item["post_text"].lower() and "access to this site" not in item["post_text"].lower() and "not acceptable" not in item["post_text"].lower() and "error" not in item["post_text"].lower():
#         new_data[item["img_url"]]=item  


# # 3. 遍历图片文件夹，找到没有文字对应的图片，删除
# filenames=os.listdir(".")
# res=[]
# files=list(set([filename.split("_")[0]+"_0" for filename in filenames if "py" not in filename and "json" not in filename]))
# for file in files:
#     if file not in new_data:
#         files.remove(file)
#         for i in range(200):
#             pass
#             try:
#                 os.remove(file.split("_")[0]+"_"+str(i)+".jpg")
#             except:
#                 pass
#     else:
#         new_data[file]["img_url"]=file+".jpg"
#         res.append(new_data[file])



# # 4. 把数据按照编号排序
# res.sort(key=lambda x: int(x["img_url"].split("_")[0]))



# # 5. 用GPT-4提取正文 (可隐去)
# for i,post in enumerate(res):
#     post_text = post["post_text"]
#     prompt='''I will give you all the text fetched from one webpage. And you need to check which part is the main body of the news (not comments, not advertisement, not related news). And extract the main body of the news. Remeber, the main body is closely related to the title( which is usually the first sentence, but you need to judge it by yourself). 
    
#     And information like this should not be deleted:\nGet back to the Sign In\nReset your password\nAn email has been sent to  with a recovery code. Please enter it below:\nEnter new password\nConfirm Password\nYour password must include:\nMin 8 characters\nMin 1 lowercase character\nMin 1 uppercase character\nMin 1 number\nSubmit\nOpen main menu button\nLife & Style\nLogin\nAccount\nSUBSCRIBE\nSearch\nNews\nFashion & Beauty\nEntertainment\nCouples\nHealth & Fitness\nHome & Living\nShop Special Issues\nPrivacy Policy\nTerms & Conditions\nLife & Style\nLogin\nAccount\nAccessibility statement\nDo Not Sell\nPrivacy Policy\nCookie Policy\nDo Not Sell\nAccessibility statement\nSocial icon facebook Social icon instagram Social icon twitter \nSearch\n\t\t\t\t\t\tSUBSCRIBE NOW!account? Login\nEm"

#     Never ever add new contents into it or use any of your own word. directly give the result without introduction and expalnation here is the text you need to clean
    
#     '''+post_text
#     try:
#         revised_version = generate_questions(prompt)
#         res[i]["post_text"]=revised_version
#     except:
#         pass
#     print(file)
#     with open("processed_data.json","w") as f:
#         json.dump(res,f)

# with open("processed_data.json","w") as f:
#     json.dump(res,f)
# print("Finished!")




# # 把乱起八糟的 1_210.jpg 等全部重命名为1_0.jpg
# # import os
# # import json
# # import sys
# # filenames=os.listdir(".")
# # for file in filenames:
# #     if not "_" in file:
# #         continue
# #     new=file.split("_")[0]+"_0."+file.split(".")[-1]
# #     try:
# #         os.rename(file, new)
# #     except:
# #         print(file)

