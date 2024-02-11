In a task of misinformation detection, two knowledge graphs are converted from the text and image of a news post, respectively. Your task is to compare two Knowledge Graphs, and determine whether image supports the text. 

The KGs are represented by a list of nodes and relationships between nodes. Each node has a name and a type that can be either 'entity' or 'event'. Each relationship is between two nodes and also have a name. Both node and entity have a weight between 0 and 1. This weight indicate the importance of the node or the entity. The first KG (generated from text) are represented by `node1` and `relationship1`, the second KG (generated from image) are represented by `node2` and `relationship2`, respectively. 

Consistency means both the entities and relations match each other.

KG:

{KG}

Output your decision and explanation in JSON format. In the "label" field, use a string to indicate your decision. "inconsistent" for confliction between the key informtion text and image. "consistent" for no inconsistencies. In the "explanation" field, output your explanation.

Below I provide several examples for you. 

**Example1 KG1**
```python
nodes1 = [
    Node('Boston Marathon', 'entity', 0.4),
    Node('Aug.15.2013', 'event', 0.15),
    Node('bombing', 'event', 0.35)
]

relationships1 = [
    Relationship(nodes[0], nodes[1], 'happen at', 0.2),
    Relationship(nodes[2], nodes[0], 'occur', 0.8)
]
```

**Example1 KG2**
```python
nodes1 = [
    Node('homemade bombs', 'entity', 0.35),
    Node('explosion', 'event', 0.45),
    Node('suspects', 'event', 0.2)
]

relationships1 = [
    Relationship(nodes[0], nodes[1], 'cause', 1),
]
```

**Example1 Label output**
{{
    "label": "support",
}}


Example output format:

{{
    "label": "support" or "not support" or "unsure",
}}

Your Decision (only output the JSON object, don't add any other words or markdown syntax like ```json):
