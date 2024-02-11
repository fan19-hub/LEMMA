In a task of misinformation detection, wwo knowledge graphs are converted from the text and image of a news post, respectively. Your task is to compare two Knowledge Graphs, and determine whether there are inconsistencies between the text and image. 

The KGs are represented by a list of nodes and relationships between nodes. Each node has a name and a type that can be either 'entity' or 'event'. Each relationship is between two nodes and also have a name. Both node and entity have a weight between 0 and 1. This weight indicate the importance of the node or the entity. The first KG (generated from text) are represented by `node1` and `relationship1`, the second KG (generated from image) are represented by `node2` and `relationship2`, respectively. 

Consistency means both the entities and relations match each other.

KG:

{KG}

Output your decision and explanation in JSON format. In the "label" field, use a string to indicate your decision. "inconsistent" for inconsistencies between the text and image. "consistent" for no inconsistencies. In the "explanation" field, output your explanation.

Example output format:

{{
    "label": "inconsistent" or "consistent",
    "explanation": "the explanation of your prediction"
}}

Your Decision (only output the JSON object, don't add any other words or markdown syntax like ```json):
