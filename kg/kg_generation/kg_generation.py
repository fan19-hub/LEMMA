import os
import openai
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """
    Node class of the knowledge graph. Each node have node_type that can either be 'entity' or 'event'. Each node also have a name attribute to indicate the name of the entity or event.
    """

    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type


class Relationship:
    """
    Relationship class of the knowledge graph. Each relationship instance represent a edge between two nodes. Each relationship also have a relationship_name attribute to indicate the what kind of relationship is between node1 and node2.
    """

    def __init__(self, node1: Node, node2: Node, relationship_name: str):
        self.node1 = node1
        self.node2 = node2
        self.relationship_name = relationship_name


def run():
    prompt = open('prompt.md', 'r', encoding='utf-8')
    prompt_text = prompt.read()
    prompt.close()

    input_file = open('input', 'r', encoding='utf-8')
    input_text = input_file.read()
    input_file.close()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an expert in Knowledge Graph generation"},
            {"role": "user", "content": prompt_text + '\n' + input_text}
        ]
    )

    with open('output', 'w', encoding='utf-8') as f:
        f.write(completion.choices[0].message['content'])


def plot(nodes, relationships):
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node.name, desc=node.name + ':' + node.node_type)
    for relationship in relationships:
        G.add_edge(relationship.node1.name, relationship.node2.name, name=relationship.relationship_name)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color='skyblue', node_size=1500, with_labels=True, font_size=10, font_weight='bold')
    plt.show()


def image_description():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "This image is extracted from a news article about The Metropolitan Police. Please describe this image in a news report tone. Don't imagine anything that is not in the image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://ichef.bbci.co.uk/news/976/cpsprodpb/AE2D/production/_131698544_db9d94b61d19957c6ce55b7381cd9ac7e2b29ed40_0_2584_35001477x2000.jpg.webp",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0])


if __name__ == '__main__':
    run()
