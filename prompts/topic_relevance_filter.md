Your task is to filter the off-topic search result. You will be provided a piece of text. You have to determine the topic of the text. Then, you will be provided the search result in JSON format. For each entry, there is a unique integer key serving as the id of each entry. The value of the each entry consists of three attributes: title, body, url. And  You have to filter the off-topic search result according to the content of the title and body. For each entry in the list, output a binary label ("true" means relevant to the topic of text, "false" means irrelevant). Put all the labels in a JSON dict

Example output format:

{{"0":true, "1":false, "2":false, "3":true, "4":false, "5":true, "6":false, "7":true}}

Text input that you are going to determine the topic:

{TEXT}

Search result in JSON format:

{SEARCH_RESULT}

Your answer (don't include the Markdown syntax like ```json. just directlt output the JSON list object. Don't output anything else):
