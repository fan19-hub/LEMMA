Your task is to convert a piece of news and an image to a knowledge graph. 

You should provide the code to construct the knowledge graph. First, I give you the class definition of Node and Relationship:

```python
class Node:
    """
    Node class of the knowledge graph. Each node have node_type that can either be 'entity' or 'event'. Each node also have a name attribute to indicate the name of the entity or event. Node also have a float number node_weight from 0 to 1 that indicate the whether this node is important or not. The higher weight, the more importance.
    """
    def __init__(self, name: str, node_type: str, node_weight: float):
        self.name = name
        self.node_type = node_type
        self.node_weight = node_weight
        
class Relationship:
    """
    Relationship class of the knowledge graph. Each relationship instance represent a edge between two nodes. Each relationship also have a relationship_name attribute to indicate the what kind of relationship is between node1 and node2. Relationship also have a float number relationship_weight from 0 to 1 that indicate the whether this relationship is important or not. The higher weight, the more importance.
    """
    def __init__(self, node1: Node, node2: Node, relationship_name: str, relationship_weight: float):
        self.node1 = node1
        self.node2 = node2
        self.relationship_name = relationship_name
        self.relationship_weight = relationship_weight
```

You should provide the code to instantiate a series of nodes and relationships that can represent the knowledge graph. Remember only include the crucial events/entities/relationships into the knowledge graph.

Make sure the sum of weights of nodes is 1 and the sum of weights of the relationships is also 1.

Remember to be fine-grained, for example, "two women" should be in two entities, not one entity named "two women". 

Below I provide an example for you. 



**News input 1**

...Jack just finishes parking and gives Tim 3 apples. ...

**Knowledge graph code output 1**

```python
nodes = [
	Node('Jack', 'entity', 0.35),
    Node('Tim', 'entity', 0.35),
    Node('apples', 'entity', 0.2),
    Node('parking', 'event', 0.1)
]

relationships = [
    Relationship(nodes[0], nodes[1], 'gives', 0.85),
    Relationship(nodes[0], nodes[3], 'finish', 0.15)
]
```

**News input 2**

"Boston Marathon bombing" occurred on April 15, 2013, near the finish line of the annual Boston Marathon in Boston, Massachusetts, United States. Two homemade bombs detonated, resulting in three deaths and several hundred injuries. The attack prompted a massive law enforcement response and a widespread investigation, ultimately leading to the identification, pursuit, and apprehension of the suspects. The incident is considered an act of terrorism.

**Knowledge graph code output 2**

```python
nodes = [
	Node('Boston Marathon', 'event', 0.35),
    Node('homemade bombs', 'entity', 0.1),
    Node('death', 'entity', 0.1),
    Node('Law enforcement', 'entity', 0.1),
    Node('Suspect', 'entity', 0.1),
    Node('Bombing', 'event', 0.25)
]

relationships = [
    Relationship(nodes[1], nodes[0], 'explode', 0.4),
    Relationship(nodes[1], nodes[2], 'cause', 0.2),
    Relationship(nodes[5], nodes[0], 'happen', 0.3),
    Relationship(nodes[4], nodes[5], 'is re', 0.1),
]
```



Now convert the following text and image into code representation of knowledge graphs, respectively You should output 2 pieces of code.

The first piece of code should be able to represent the text, with node and relationship stored in `node1` and `relationship1` respectively.

The second piece of code should be able to represent the image, with node and relationship stored in `node2` and `relationship2` respectively.

**Use the mark '---' to separate the code.**

An example of the output format is shown below:

```python
nodes1 = [
    ...
]

relationships1 = [
    ...
]
```
---
```python
nodes2 = [
    ...
]

relationships2 = [
    ...
]
```
Only output the code, do not output anything else.

**News Input**

{TEXT}

The image is also provided. 

**Knowledge graph code output**
