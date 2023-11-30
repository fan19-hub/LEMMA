Your task is to check whether the given KG has logical confliction with the given text: 

The given KG is generated from the image corresponding to the given text.

The KGs are represented by a list of nodes and relationships between nodes. Each node has a name and a type that can be either 'entity' or 'event'. Each relationship is between two nodes and also have a name. Both node and entity have a weight between 0 and 1. This weight indicate the importance of the node or the entity. The KG (generated from image) are represented by `node1` and `relationship1`. 

You should go through each node and relationship in given KG to check where exists logical confliction with given text.

Note that **no mention**, **no indication** doesn't mean logical confliction between kg and text. However, if some entities or relationships OBVIOUSLY disobey the context text, this means logical confliction.
 
KG: 

{KG}

Original text:

{ORIGINALTEXT}

Output your prediction and explanation. In the first line of the output, use a float number between 0 or 1 to indicate your predicted confidence. 0 for logical confliction. 1 for no logical confliction. The number should Keep two decimal places. For example, 0.65. In the second line or more lines, output your explanation.

Your Prediction: