You are given a piece of **Input Text** and an image caption. Your task is to predict whether misinformation is present. The text and the image come from the same post (or the same news report), where the text serves as the content, and the image complements or provides evidence for the text. By assessing the consistency between the text and the image, please predict whether this is a post containing misinformation. Please follow the Rules below:

# Rules:
1. Start your reasoning with an evaluation based on the sentence 'Let's think step by step'.
2. Output your complete reasoning in the subsequent lines.
3. In the final line, use a single word to indicate whether misinformation exists, which should be selected from ["Real", "Fake"].
"Real" indicates that no misinformation is detected. 
"Fake" indicates that misinformation is detected. 

# Input Text:

{TEXT}

# Image Caption:

{CAPTION}

# Your Response:
Let's think step by step, 
