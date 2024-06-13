You are given a Query. You are then given a dictionary called Documents, whose key is the document ID and value is the documen retrieved from the Internet. For each document, 
- if some segments are relevant to any key information in Query, quote them.
- if the whole page is relevant to Query, summarize it comprehensively and concisely
- if it is irrelevant to Query, return empty string
Please output a new dictionary, whose key is still document ID and value is the document segments relevant to the Query. Try to only include the relevant part instead of returning the whole thing back.But do not be too strict.

### Example output format
{{"0":"Funding has been awarded to nine pioneering projects to help Scottish remanufacturing businesses make the most efficient use of material. The Scottish", "1":"New Institute of Remanufacture to drive Scotland's circular economy","2": "'The Scottish Government defines a circular economy as a system in which “resources are kept in use for as long as possible” – in other words, recycling.","3":"Our circular economy strategy to build a strong economy, protect our resources and support the environment."}}

### Your turn

**Query**
{TEXT}

**Documents**
{EVIDENCE}

**Output: (Don't output anything else except for the JSON object. Don't add Markdown syntax like ```json):**
