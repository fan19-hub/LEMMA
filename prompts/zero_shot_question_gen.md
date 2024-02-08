You are given a piece of **Input Text** and an **image**. Your task is to predict whether misinformation is present. The text and the image come from the same post (or the same news report), where the text serves as the content, and the image complements or provides evidence for the text. By assessing the consistency between the text and the image, please predict whether this is a post containing misinformation. Please follow the Rules below:

### Rules:

Generate a JSON object with four properties: 'label', 'explanation', 'title', 'questions'. 

The 'label' property should be a binary value of 0 or 1, where 0 indicates that no misinformation is detected and 1 indicates that misinformation is present. 

The 'explanation' property should provide a detailed reasoning for the given 'label'. 

However, reasoning merely based on the input text and image might not be sufficient to make predictions. Please also come up with a title for this news, then list two questions/phrases/sentences that  when searched on search engines, would produce the most pertinent results to refine your prediction and reasoning. Store the title in the 'title' field and questions in the 'questions' field. Please use English to generate your title and questions. However, if the text of news/post in written in Chinese, you should use Chinese to generate your title and questions. No other words or elements should be included in the output apart from these four properties. And do not add Markdown syntax like ```json, just only output the json object.

### Example 1:

**Text Input**

is baltimores prosecutor wrong about freddie grays legal knife the weapon police described is definitely illegalso why did marilyn mosby say it wasnt the answer hinges on a single spring

**Expected Output (JSON)**

{{
    "label": 1,
    "explanation": "The image shows a protest sign with the text 'JUSTICE FOR FREDDIE' and a background of multiple images of a man's face, which seems to be related to a call for justice for Freddie Gray. However, the image does not provide any information about the legality of the knife in question or any details about the specific claims made by the Baltimore prosecutor, Marilyn Mosby. Therefore, the image does not corroborate or contradict the text's claim about the legality of the knife, and it does not provide evidence to support the text's discussion of the weapon's legality. The lack of relevant information in the image to assess the text's claim about the knife suggests that the post may contain misinformation.",
    "title":"Freddie Gray's Knife: Legal or Not?",
    "questions":[
        "Was Freddie Gray's knife legal?", 
        "Marilyn Mosby's comments on Freddie Gray’s Legal Knife"
    ]
}}

### Example 2:

**Text Input**

RT @danrem: Konon, inside The Bataclan concert before the attack. How life can change in a second. #Pray4Paris

**Expected Output (JSON)**

{{
    "label": 0,
    "explanation": "The image shows a concert venue with a crowd of people, which is consistent with the text mentioning The Bataclan concert before the attack. The image and the text both depict a scene prior to a tragic event, and there is no clear discrepancy that would indicate misinformation.",
    "title":"Inside The Bataclan Concert Moments Before the Attack",
    "questions":[
        "the full story of what happened in the Bataclan | Paris attacks", 
        "Authenticity of images from Bataclan before the attack"
    ]
}}

### Your Turn

**Text Input**

{TEXT}

Image is provided.

Your Response:
