import json
import random
import time

import requests
from utils import stats
from toolLearning import text_search
from lemma_component import LemmaComponent

if __name__ == '__main__':
    data = {
        "text": "RT @europapress: Los refugiados intentan zafarse del estigma de Colonia (Alemania)  https://t.co/zoe8JNNaAK vía @EPinternacional https://t.…",
        "image_url": "twitter/Mediaeval2016_TestSet_Images/protest_6.jpg",
        "tool_learning_text": "{\"Refugees in Cologne Attempt to Overcome Stigma\": [\"Los refugiados intentan zafarse del estigma de Colonia (Alemania)\"], \"Refugee situation in Cologne Germany\": [{\"title\": \"Cologne attacks: Support for refugees in Germany falling amid far-right ...\", \"href\": \"https://www.independent.co.uk/news/world/europe/cologne-attacks-support-for-refugees-in-germany-plummeting-amid-farright-protests-and-vigilante-attacks-a6808616.html\", \"body\": \"Germany's welcoming attitude to refugees is fading fast following the New Year's Eve attacks on women in Cologne, according to new research. In Novemb\"}, {\"title\": \"The end of 'Welcome Culture'? How the Cologne assaults reframed Germany ...\", \"href\": \"https://journals.sagepub.com/doi/pdf/10.1177/02673231211012173\", \"body\": \"welcome a hostel for refugees in their own neighbourhood in November 2015 (Liebe et al., 2018: 3). However, while opposition to local refugee resettle\"}, {\"title\": \"Five years on: How Germany's refugee policy has fared\", \"href\": \"https://www.dw.com/en/five-years-on-how-germanys-refugee-policy-has-fared/a-54660166\", \"body\": \"Five years ago, as hundreds of thousands of refugees came to Germany, Chancellor Angela Merkel maintained: \\\"We can do this!\\\" How has Germany — and tho\"}], \"Public perception of refugees in Cologne after incidents\": [{\"title\": \"The end of 'Welcome Culture'? How the Cologne assaults reframed Germany ...\", \"href\": \"https://journals.sagepub.com/doi/pdf/10.1177/02673231211012173\", \"body\": \"welcome a hostel for refugees in their own neighbourhood in November 2015 (Liebe et al., 2018: 3). However, while opposition to local refugee resettle\"}, {\"title\": \"Cologne attacks show Germany unprepared for migration challenge\", \"href\": \"https://www.reuters.com/article/us-europe-migrants-germany-challenges-in-idUSKCN0V6173\", \"body\": \"The incidents have caused profound soul searching in a country that allowed in an unprecedented 1.1 million migrants last year in what its leaders des\"}, {\"title\": \"After Cologne, is Germany's refugee welcome kaput? | CBC News\", \"href\": \"https://www.cbc.ca/news/world/cologne-refugees-don-murray-1.3402376\", \"body\": \"The assaults on German women in Cologne on New Year's Eve, incidents being blamed largely on foreigners, has fuelled anti-immigrant sentiment right ac\"}]}",
        "label": 0,
        "prediction": 1,
        "explain": "Based on the new references provided, it is clear that the original text of the news from Europa Press discusses refugees in Cologne, Germany, attempting to overcome the stigma associated with them, particularly after the incidents on New Year's Eve. The external resources confirm that there was a significant shift in public perception and support for refugees in Germany following these events, with increased opposition and soul-searching within the country.\n\nThe image in question shows a protest sign with a derogatory message about refugees, which is a strong visual element that could evoke a negative emotional response. This image, when paired with the text about refugees trying to shake off the stigma, creates a false connection. The image depicts the very stigma that the refugees are trying to escape, rather than an effort to overcome it. Therefore, the image does not support the message of the text, which is about refugees attempting to rid themselves of stigma. Instead, it shows the opposition they face, which could lead to a misunderstanding of the text's intent if the two are viewed together.\n\nGiven the definitions provided, the news should be classified as containing a \"False Connection\" because there is a disconnect between the information conveyed by the image and the essential details provided in the accompanying text.\n\nFalse Connection",
        "direct": 1,
        "direct_explain": "The image shows a protest sign with a derogatory message about refugees, which is a strong visual element that could be used to evoke a negative emotional response. The text, however, mentions refugees trying to shake off the stigma of Cologne (Germany), which implies a context of overcoming negative perceptions or incidents. The image does not support the text's message of refugees attempting to rid themselves of stigma; instead, it depicts the very stigma that they would be trying to escape. This inconsistency suggests that the image is being used to misrepresent the situation or the sentiment of the text, which could lead to misinformation."
    }

    module_no_cap = LemmaComponent(prompt='kg_gen_no_cap_prompt.md', name='kg_gen2', model='gpt4v', using_cache=False,
                                   online_image=True, max_retry=3, max_tokens=1000, temperature=0.1)

    module_kg_comp = LemmaComponent(prompt='kg_comp_prompt_new.md', name='kg_comp', model='gpt4', using_cache=False,
                                    online_image=True, max_retry=3, max_tokens=1000, temperature=0.1)
    # temp = LemmaComponent(prompt='test.md', name='temp', model='gpt4v', using_cache=False,
    #                       online_image=True, max_retry=3, max_tokens=1000, temperature=0.1)

    result = module_no_cap(TEXT=data['text'], image=data['image_url'])
    print(result)
    result = module_kg_comp(KG=result)
    print(result)
    # result = temp(TEXT=data['text'], image=data['image_url'])
    # print(result)
