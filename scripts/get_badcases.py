import json
with open("out/lemma_twitter_output.json", "r",encoding="utf-8") as f:
    outputs = json.loads(f.read())


with open("data/badcase.json","r",encoding="utf-8") as f:
    results = json.loads(f.read())
posts_set = set([result["original_post"] for result in results])

for output in outputs:
    if (output["label"] != output["prediction"]) and (output["text"] not in posts_set):
        output["original_post"] = output["text"]
        output.pop("text",None)
        results.append(output)

with open("data/badcase.json","w", encoding="utf-8") as f:
    f.write(json.dumps(results))

# import json
# with open("out/lemma_twitter_output.json", "r",encoding="utf-8") as f:
#     outputs = json.loads(f.read())


# with open("data/badcase.json","r",encoding="utf-8") as f:
#     results = json.loads(f.read())
# posts_set = set([result["original_post"] for result in results])

# results = []
# for output in outputs:
#     # if (output["label"] != output["prediction"]) and (output["text"] not in posts_set):
#     if (output["label"] == output["prediction"]) and output["tool_learning_text"]==None:
#         output["original_post"] = output["text"]
#         output.pop("text",None)
#         results.append(output)

# with open("data/case1.json","w", encoding="utf-8") as f:
#     f.write(json.dumps(results))

