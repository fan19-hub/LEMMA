You are given a piece of **Reasoning** about the first-stage decision of the authenticity of multimedia news post, the **Text** is the text part of the post and you have already get the image part of the post. Your task is to decide whether additional evidences are needed for predicting whether misinformation is present.

For deciding whether additional evidences are needed, please focus on two things:
1. Whether the authenticity of events is verified.
2. Whether authenticity of image is suspicious.


You should only respond in format as described below. DO NOT RETURN ANYTHING ELSE. START YOUR RESPONSE WITH '{{'.
[response format]: 
{{
    "explanation": "Why the additional evidences is needed or not?"
    "external knowledge": "Yes" if the you think additional evidences are needed, "No" otherwise.
}}


Input Reasoning:

{REASONING}

Input Text:

{TEXT}

Your Response: