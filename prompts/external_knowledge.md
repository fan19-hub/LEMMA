You are given a piece of **Reasoning** about the first-stage decision of the authenticity of multimedia news post, the **Text** is the text part of the post and you have already got the image part of the post. Your task is to decide whether additional evidence is needed for predicting whether misinformation is present.

For deciding whether additional evidences are needed, please focus on two things:
1. Whether the authenticity of events is suspicious.
2. Whether the authenticity of the image is suspicious.

Note that you should not easily judge that one post is "true", normally you need more external resources.

You should only respond in format as described below. DO NOT RETURN ANYTHING ELSE. START YOUR RESPONSE WITH '{{'.
[response format]:
{{
   "explanation": "Why is the additional evidence needed or not?"
   "external knowledge": "Yes" if you think additional evidence is needed, "No" otherwise.
}}


Input Reasoning:

{REASONING}

Input Text:

{TEXT}

Your Response: