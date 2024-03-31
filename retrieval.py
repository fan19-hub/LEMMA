
import re
import json

from time import sleep

from newspaper import Article
from langdetect import detect
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

import openai
from openai import OpenAI

from utils import predict_region
from configs import prompts_root,OPENAI_KEY


# Setup OpenAI API
openai.api_key = OPENAI_KEY
client = OpenAI()

untrusted_sources={"www.facebook.com","m.facebook.com","www.reddit.com","www.weibo.com","twitter.com","www.tiktok.com","www.douyin.com","www.instagram.com","www.pinterest.com","www.taobao.com","www.jd.com","www.amazon.com","www.ebay.com","www.imdb.com","www.douban.com","steamcommunity.com","m.ixigua.com","www.bilibili.com","www.netflix.com",}

def soure_filter(results):
    global untrusted_sources
    if results == None or results == []:
        return []
    for result in results:
        link=result['href']
        domain = re.search('https?://([A-Za-z_0-9.-]+).*', link).group(1)
        if domain in untrusted_sources:   
            results.remove(result)
    return results



def topic_relevance_filter(text, all_results, top_k, query_set, cutoff_index=150):
    # Structure flattern
    all_results_flatterned = []
    for qid, query in enumerate(all_results.keys()):
        results= all_results[query]
        for i,result in enumerate(results):
            id = qid*top_k + i        # we can use id//top_k to determine which query it belongs later
       
            result['body']=result['body'][:cutoff_index]
            all_results_flatterned.append({id:result})

    # Prompt formation
    text=text[:cutoff_index]
    with open(prompts_root+'topic_relevance_filter.md', 'r', encoding='utf-8') as f: 
        prompt=f.read()
    prompt=prompt.format(TEXT=text, SEARCH_RESULT=json.dumps(all_results_flatterned, ensure_ascii=False, indent=4))

    # GPT Query
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    response = completion.choices[0].message.content

    # Post process
    try:
        relevance_labels=json.loads(response)
    except:
        # print("Tool learning Warning: Invalid response from topic_relevance_filter. Remain unchanged.")
        return results
    
    # Wash the string keys to int, and remove the non-integer keys
    temp = {}
    for id, value in relevance_labels.items():
        if type(id)==str: 
            if id.isdigit(): 
                id=int(id)
            else: continue
        temp[id] = value
    relevance_labels = temp
        
    # Filter the results and restructure the results
    all_filtered_results = {}  
    for temp in all_results_flatterned:
        id, result = list(temp.items())[0]
        if id in relevance_labels and relevance_labels[id]==True:
            qid=id//top_k               # use id//top_k to determine which query it belongs
            query=query_set[qid]
            try:
                all_filtered_results[query].append(result)
            except:
                all_filtered_results[query]=[result]
    return all_filtered_results


def scraper(url, max_len=2000):
    if url == None or url == "" or "http" not in url:
        return ""
    
    try:
        article = Article(url)
    except Exception as e:
        print(f"Tool learning Warning: scraper failed on {url}. {e}")
        return ""
    try: article.download()
    except Exception as e:
        sleep(10)
        try: article.download()
        except:
            print(f"Tool learning Warning: scraper failed on {url}. {e}")
            return ""
    try: article.parse()
    except Exception as e:
        print(f"Tool learning Warning: scraper failed on {url}. {e}")
        return ""

    publish_date=article.publish_date
    text=article.text
    body_text = f"publish date: {publish_date}\n\n{text}"
    body_text = body_text[:max_len]
    return body_text
    


def text_search(query, query_type="title", top_k=5):
    # Prefix
    region = predict_region(query)
    prefix = 'fake news '
    if query_type =='title':
        query = prefix + query

    # DuckDuckGo Search
    max_results = 2*top_k
    # with DDGS() as ddgs:
    try:
        results=list(DDGS().text(query, 
                            region=region, 
                            safesearch='off', 
                            max_results=max_results))
    except DuckDuckGoSearchException as e:
        print(e)
        return []
    if not results: 
        return []

    # Source Filter
    results = soure_filter(results)
    return results[:top_k]



def evidence_extraction(search_results, query, pre_max_len=2000, after_max_len=250):
    full_text_results = []
    for search_result in search_results:
        title = search_result['title']
        link = search_result['href']
        full_text = scraper(link,pre_max_len)
        full_text = f"[title]: {title}\n"+full_text
        full_text_results.append(full_text)
    with open("full_text_results.json", 'w', encoding='utf-8') as f: 
        f.write(json.dumps(full_text_results, ensure_ascii=False, indent=4))
    
    # Prompt formation
    with open(prompts_root+'evidence_extraction.md', 'r', encoding='utf-8') as f: 
        prompt=f.read()
    prompt=prompt.format(EVIDENCE = json.dumps(full_text_results), TEXT = query)
    
    # GPT Query
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    response = completion.choices[0].message.content
    try:
        evidences=json.loads(response)
        evidences=list(evidences.values())[0]
    except:
        print("Tool learning Warning: Invalid response from evidence_extraction. Remain unchanged.")
        evidences=full_text_results
    with open("evidences.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(evidences, ensure_ascii=False, indent=4))
    evidences=[evidence[:after_max_len] for evidence in evidences if len(evidence)>0]
    return evidences
    

def get_evidence(text, title, questions, max_len=2000):
    # Query processing
    top_k=5
    query_set = [title] + questions
    get_query_type = ['title'] + ['question']*len(questions)
    all_search_results = {}
    for qid, query in enumerate(query_set): 
        # Query Type
        q_type=get_query_type[qid]
        # Text Search
        results=text_search(query, q_type, top_k)

        # Results Formatting
        for result in results:
            try:
                all_search_results[query].append(result)
            except:
                all_search_results[query]=[result]

    # Topic Relevance Filter
    enhanced_text=f"[title]:{title}\n{text}"
    all_search_results = topic_relevance_filter(enhanced_text, all_search_results, top_k, query_set)
    
    # Evidence Extraction
    evidences=evidence_extraction(all_search_results[title], enhanced_text)
    all_search_results[title]=evidences
    return json.dumps([value for value in all_search_results.values()])



# Unit test:
# if __name__ =="__main__":
#     text="'cash backing to remake scotland a wastefree economy the cash is from the scottish institute for remanufacture supported by the government to create a wastefree circular economy remanufacturing is a process that takes old but highvalue products and restores them to an asnew condition'"
#     title="Scotland's Investment in Waste-Free Circular Economy"
#     questions=['Scottish Institute for Remanufacture government funding', 'Success stories of remanufacturing in Scotland']
#     get_evidence(text, title, questions)    
#     scraper("https://www.bbc.com/news/world-us-canada-68244352", 2000)

