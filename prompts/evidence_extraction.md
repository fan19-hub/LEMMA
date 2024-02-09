You are given a piece of news/post. You are then provided a list of webpages retrieved from the Internet. For each webpage, please quote or summarize the text fragments that are relevant to the news/post. Return the quoted/summarized text as a new string. If the entire evidence is irrelevant to the news/post, please return an empty string. Try your best to only include the relevant fragment instead of returning the whole thing back. At the same time, do not waste any valuable information.

### Example:


**News/Post:**
news/post text

**Webpages:**

[
    "relevant webpage 1",
    "irrelevant webpage 2",
    "relevant webpage 3"
]

**Output:**
{{
    "results": [
                "text in webpage 1 that is relevant to the news/post",
                "",
                "summary of content in webpage 3 that is relevant to the news/post"
                ]
}}

### Your turn

**News/Post:**

{TEXT}

**Webpages:**

{EVIDENCE}

**Output: (Don't output anything else except for the JSON object. Don't add Markdown syntax like ```json):**
