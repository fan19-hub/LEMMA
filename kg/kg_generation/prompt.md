Your task is to convert a piece of news report to a knowledge graph. 

You shell provide the code to construct the knowledge graph. First, I give you the class definition of Node and Relationship:

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

You should provide the code to instantiate a series of nodes and relationships that can represent the knowledge graph.

Remember to be fine-grained, for example, "two women" should be in two entities, not one entity named "two women". 

Below I provide an example for you. 



**News input**

...Maduro was not targeted by the drones, the prime minister said, but state security services reported that the drones were meant for him. "The explosion was caused by two machine guns," Maduro said, adding that there were no injuries. ...

**Knowledge graph code output**

```python
nodes = [
	Node('Maduro', 'entity', 0.3),
    Node('drones', 'entity', 0.7),
    Node('targeted', 'event', 0.7),
    Node('guns', 'entity', 1),
    Node('explosion', 'event', 0.8)
]

relationships = [
    Relationship(nodes[0], nodes[2], 'victim', 0.5),
    Relationship(nodes[1], nodes[2], 'device', 0.5),
    Relationship(nodes[3], nodes[4], 'explosive device', 0.8),
]
```



Now convert the following text into code representation of knowledge graph.

**News input**
