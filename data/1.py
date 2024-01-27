import json
root=r"weibo\rumor_images"
with open("test.json","r") as f:
#    t= f.read()
   a=json.load(f)
print(a)
