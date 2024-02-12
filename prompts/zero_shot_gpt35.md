You are given a piece of **Input Text** and an image caption. Your task is to predict whether misinformation is present. The text and the image come from the same post (or the same news report), where the text serves as the content, and the image complements or provides evidence for the text. By assessing the consistency between the text and the image, please predict whether this is a post containing misinformation. Please follow the Rules below:

Rules:
Generate a JSON object with two properties: 'label', 'explanation'. 
The return value of 'label' property should be selected from ["Real", "Fake"].
"Real" indicates that no misinformation is detected. 
"Fake" indicates that misinformation is detected. 
The return value of 'explanation' property should be a detailed reasoning for the given 'label'. 

Note that your response will be passed to the python interpreter, SO NO OTHER WORDS! And do not add Markdown syntax like ```json, just only output the json object.

Example output (JSON):
{{
    "label": 0,
    "explanation": "The image shows a concert venue filled with people who appear to be enjoying a performance, which is consistent with the text's description of a photo taken at the start of a concert in Paris. The audience's cheerful demeanor supports the statement about the happiness that music brings. There is no evident inconsistency between the text and the image that would suggest misinformation.",
}}

Input Text:

{TEXT}

Image Caption:

{CAPTION}

Your Response:
