import json

json2 = 'out/fakereddit_lemma_base_kg_final_output_full.json'
with open(json2, 'r') as json_file:
    data = json.load(json_file)

label = []
direct = []
pred = []
for ele in data:
    label.append(ele['label'])
    direct.append(ele['direct'])
    pred.append(ele['prediction'])

print("label=",label)
print("direct=",direct)
print("prediction=",pred)