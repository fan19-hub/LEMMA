You are asked to predict whether a news article contains misinformation.

The text of this news is:

{{TEXT}}

Your original prediction is {{PREDICTION}}. (0 for no misinformation, 1 for presence of misinformation)

However, external sources can better help you make the judgement. Please list three questions that you would like to search on a public search engine, such as Google. Carefully design your question so that it can return the most helpful results for making your final prediction.

Output format (JSON):
{{
    "questions": [
        "",
        "",
        ""
    ]
}}

Don't output quotation marks, just only output the json object. Your response:

