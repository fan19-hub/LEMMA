

Your task is to figure out whether a Weibo post contains misinformation. Sometimes the text and image of a post might contain fake information and one might be able to figure it out if the information of text and image does not match. 

To help you with the task, you are provided with three Knowledge Graphs. The first KG is converted from the text part of a post on Weibo.com. The second KG is converted from the image corresponding to the same post. The third KG is converted from some relevant facts and information, and can be trusted. This is used for your general references. 

Compare the first two Knowledge Graphs, and determine whether the post contains misinformation, based on the first two Knowledge Graphs match or not.

Here are some techniques that you should use to determine whether text and image matches:

- Are there common features in the two KGs? 
- Although the first (second) KG have nodes and relationships that the second (first) KG not have, can there be any possibilities that they are correlated?
- Does the first two KGs contains nodes and relationships that are totally contradicted to the third (fact) KG? Note that if some nodes and relationships of the first two KGs are not exists in the third KG or the third KG contains nodes and relationships that are not in the first two KGs, this is not necessarily a contradict. Contradiction means some nodes in the first two KGs and the nodes in the fact KG are expressing exactly the different logic.

The KGs are represented by a list of nodes and relationships between nodes. Each node has a name and a type that can be either 'entity' or 'event'. Each relationship is between two nodes and also have a name. Both node and entity have a weight between 0 and 1. This weight indicate the importance of the node or the entity. The first KG (generated from text) are represented by `node1` and `relationship1`, the second KG (generated from image) are represented by `node2` and `relationship2`, and so on. 

Note that if some entities only exist in one of the first two KGs, it does not necessarily means misinformation exists. It might be the image does not captures all the details mentioned in the text. You can use the weight to help your prediction. 

You are also provided with the original text and image (converted to text description). You can use them to help you make the prediction.

KG:

{KG}

Original text:

{ORIGINALTEXT}

Output your prediction and explanation. In the first line of the output, use a float number between 0 or 1 to indicate your predicted probability of misinformation exists. 0 for no misinformation. 1 for misinformation do exist. The number should Keep two decimal places. For example, 0.51. In the second line or more lines, output your explanation.

Your Prediction:

