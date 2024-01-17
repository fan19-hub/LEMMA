You are given a piece of text and an image (already converted into textual description). Your task is to predict whether misinformation is present. The text and the image come from the same Weibo post, where the text serves as the content, and the image complements or provides evidence for the text. By assessing the match between the text and the image, you can predict whether this is a post containing misinformation. You should also take general knowledge into consideration. Output your prediction and explanation. In the first line of the output, use a single binary value 0 or 1 to indicate whether misinformation exists. 0 for no misinformation. 1 for misinformation do exist. In the second line or more lines, output your explanation.

Text:

{TEXT}

Image (converted into textual description):

{IMAGE}

Your Prediction: