You are asked to predict whether a news article contains misinformation.

The text of this news is:

{TEXT}

External sources can better help you make the judgement. Please come up with a title for this news first, then list two questions/phrases/sentences that you would like to search on a public search engine, such as Google. Carefully design your question so that it can return the most helpful results for making your final prediction and reasoning. Please use English to generate your title and questions. 

Text Input example 1:

is baltimores prosecutor wrong about freddie grays legal knife the weapon police described is definitely illegalso why did marilyn mosby say it wasnt the answer hinges on a single spring

Output example (JSON) 1:
{{
    "title":"Freddie Gray's Knife: Legal or Not?",
    "questions":[
        "Was Freddie Gray's knife legal?", 
        "Marilyn Mosby's comments on Freddie Gray’s Legal Knife"
    ]
}}

Text Input example 2:

RT @danrem: Konon, inside The Bataclan concert before the attack. How life can change in a second. #Pray4Paris

Output example (JSON) 2:
{{
    "title":"Inside The Bataclan Concert Moments Before the Attack",
    "questions":[
        "the full story of what happened in the Bataclan | Paris attacks", 
        "Authenticity of images from Bataclan before the attack"
    ]
}}

Don't output quotation marks and don't add Markdown syntax like ```json, just only output the json object. Your response:
