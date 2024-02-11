Your task is to compare two Knowledge Graphs, and determine whether some misinformation exist in any of the Knowledge Graphs. 

The first KG is converted from the text part of a post on Weibo.com. The second KG is converted from the image corresponding to the same post. 

Sometimes the text and image might contain fake information and one might be able to figure it out if the information of text and image does not match. Here are some techniques that you should use to determine whether text and image matches:

- Are there common features in the two KGs? 
- Although the first KG have nodes and entities that the second KG not have, can there be any possibilities that they are correlated?

The KGs are represented by a list of nodes and relationships between nodes. Each node has a name and a type that can be either 'entity' or 'event'. Each relationship is between two nodes and also have a name. Both node and entity have a weight between 0 and 1. This weight indicate the importance of the node or the entity. The first KG (generated from text) are represented by `node1` and `relationship1`, the second KG (generated from image) are represented by `node2` and `relationship2`, respectively. 

Note that if some entities only exist in one KG, it does not necessarily means misinformation exists. It might be the image does not captures all the details mentioned in the text. You can use the weight to help your prediction. 

You are also provided with the original text and image (converted to text description). You can use them to help you make the prediction.

KG:

{KG}

Original text:

{ORIGINALTEXT}

Output your prediction and explanation. In the first line of the output, use a float number between 0 or 1 to indicate your predicted probability of misinformation exists. 0 for no misinformation. 1 for misinformation do exist. The number should Keep two decimal places. For example, 0.65. In the second line or more lines, output your explanation.

Your Prediction:

