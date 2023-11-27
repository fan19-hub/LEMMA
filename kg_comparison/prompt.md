Your task is to compare two Knowledge Graphs, and determine whether some misinformation exist in any of the Knowledge Graphs. 

The first KG is converted from the text part of a post on Weibo.com. The second KG is converted from the image corresponding to the same post. 

Sometimes the text and image might contain fake information and one might be able to figure it out if the information of text and image does not match. Your task is to predict a binary label to indicate whether text and image matches. Also provide a explanation of your prediction.

The KGs are represented by a list of nodes and relationships between nodes. Each node has a name and a type that can be either 'entity' or 'event'. Each relationship is between two nodes and also have a name.

You are also provided with the original text and image (converted to text description). You can use them to help you make the prediction.

