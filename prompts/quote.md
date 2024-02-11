You are given a piece of news/post. You are then provided a list of evidences retrieved from the Internet. For each evidence, please quote the information that are relevant to the news/post. Return the quoted/summarized text as a new string. If the entire evidence is irrelevant to the news/post, please return an empty string.

### Example:

**News/Post:**

news/post text

**Evidence:**

{{
[
    "evidence 1",
    "evidence 2",
    "evidence 3"
]
}}

**Output:**

{{
[
    "text in evidence 1 that is relevant to the news/post",
    "text in evidence 2 that is relevant to the news/post",
    "text in evidence 3 that is relevant to the news/post"
]
}}

### Your turn

**News/Post:**

{TEXT}

**Evidence:**

{EVIDENCE}

**Output (Don't output anything else except for the JSON object. Don't add Markdown syntax like ```json):**
