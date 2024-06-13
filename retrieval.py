
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
from urllib.parse import urlparse

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from configs import imgbed_root
import os
chrome_driver_path = 'chromedriver.exe'

# Find the chromederver suitable for your chrome version here: https://googlechromelabs.github.io/chrome-for-testing/#stable

# Initialize the Chrome webdriver and open the URL
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome()


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
    text=text[:cutoff_index+50]
    with open(prompts_root+'topic_relevance_filter.md', 'r', encoding='utf-8') as f: 
        prompt=f.read()
    prompt=prompt.format(TEXT=text, SEARCH_RESULT=json.dumps(all_results_flatterned, ensure_ascii=False, indent=4))

    # GPT Query
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
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
    for query in query_set:
        all_filtered_results[query]=[]
    for temp in all_results_flatterned:
        id, result = list(temp.items())[0]
        if id in relevance_labels and relevance_labels[id]==True:
            qid=id//top_k               # use id//top_k to determine which query it belongs
            query=query_set[qid]
            all_filtered_results[query].append(result)
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



def evidence_extraction(search_results, query, pre_max_len=2000, after_max_len=250, max_items = 3):
    documents = {}
    headers = {}
    for id, search_result in enumerate(search_results):
        title = search_result['title']
        link = search_result['href']
        body = search_result["body"]
        full_text = scraper(link,pre_max_len)
        if len(full_text)<30:
            documents[str(id)] = body
        else:  
            documents[str(id)] = full_text
        #  Source: {urlparse(link).hostname}
        headers[str(id)] = f"Title: {title}."

    # Prompt formation
    with open(prompts_root+'evidence_extraction.md', 'r', encoding='utf-8') as f: 
        prompt=f.read()
    prompt=prompt.format(EVIDENCE = json.dumps(documents), TEXT = query)
    
    # GPT Query
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    response = completion.choices[0].message.content

    evidences = []
    try:
        extracted_results=json.loads(response)
        for id, extracted_result in extracted_results.items():
            if extracted_result != "":
                evidence = headers[str(id)] + extracted_result 
                evidences.append(evidence)
    except:
        print("Tool learning Warning: Invalid response from evidence_extraction. Remain unchanged.")
        evidences = list(documents.values())
    # with open("logging/evidences.json", 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(evidences, ensure_ascii=False, indent=4))
    evidences=[evidence[:after_max_len] for evidence in evidences if len(evidence)>0]
    return evidences[:max_items]
    

def get_evidence(text, title, questions, max_len=2000):
    # Query processing
    top_k=5
    query_set = [title] + questions
    get_query_type = ['title'] + ['question']*len(questions)
    all_search_results = {}
    titles_seen = set()
    for qid, query in enumerate(query_set): 
        # Query Type
        q_type=get_query_type[qid]
        # Text Search
        results=text_search(query, q_type, top_k)

        # Results Formatting
        for result in results:
            if result['title'] in titles_seen: continue
            else: titles_seen.add(result['title'])
            try:
                all_search_results[query].append(result)
            except:
                all_search_results[query]=[result]

    # logging
    search_log = {"original_post":text, "title":title, "questions":questions, "original_search_results":all_search_results}

    # Topic Relevance Filter
    enhanced_text =f"Title: {title}. \n {text}"
    all_search_results = topic_relevance_filter(enhanced_text, all_search_results, top_k, query_set)
    search_log["relevant_search_results"]=all_search_results
    # Evidence Extraction
    all_search_results[title]=evidence_extraction(all_search_results[title], enhanced_text)

    # Formatting
    retrieved_dict = {f"Infomation might relate to '{title}'":json.dumps(all_search_results[title])}
    all_search_results.pop(title,None)
    for question, evidences in all_search_results.items():
        info_list = [] 
        for evidence in evidences[:2]:
            # Source: {urlparse(evidence['href']).hostname}
            info_list.append(f"Title: {evidence['title']}.\n {evidence['body']}")
        retrieved_dict[f"Infomation might relate to '{question}'"] = info_list

    # logging
    search_log["retrieved_text"] = retrieved_dict
    with open("logging/search_results.json", 'a', encoding='utf-8') as f: 
        f.write(json.dumps(search_log, ensure_ascii=False, indent=4))

    return json.dumps(retrieved_dict)


def visual_search(source, original_post, is_url=True, max_items = 5):
    # Google Image Search Page
    try:
        driver.get('https://www.google.com/imghp')
    except:
        try:
            driver.quit()
        except:
            pass
        driver = webdriver.Chrome()
        driver.get('https://www.google.com/imghp')
    sleep(1)  
    button = driver.find_element(By.CSS_SELECTOR, "div.nDcEnd")
    button.click()
    sleep(1) 

    # Get the image
    if is_url:
        # use the image url
        if "http" not in source: 
            source=imgbed_root+source
        driver.find_element(By.CSS_SELECTOR, "input.cB9M7").send_keys(source)
        search_button=driver.find_element(By.CSS_SELECTOR, "div.Qwbd3")
        search_button.click()       
    else:
        # upload the image
        image_path=os.path.abspath(source) 
        pyautogui.typewrite(image_path)
        sleep(3)  
        pyautogui.press('enter')
        pyautogui.press('enter')
        sleep(5)  
        driver.find_element_by_name('file').send_keys(r"D:\test\xuexi\test\14.png")
        upload_button = driver.find_element(By.CSS_SELECTOR, "div.ZeVBtc>span")
        upload_button.click()

    sleep(1)
    # image serach result page
    exact_search=driver.find_element(By.CSS_SELECTOR, "div.ICt2Q")
    exact_search.click()
    sleep(2)

    # exact search result page
    results=driver.find_elements(By.CSS_SELECTOR, "li>a")
    search_results=[]
    for result in results:
        link = result.get_attribute('href')
        if "google.com" in link:
            continue
        title = result.get_attribute('aria-label')
        if title !="":
            # "source":urlparse(link).hostname
            search_result= "Title: " + title.replace("来源","Source")
            search_results.append(search_result)
    if search_results==[]:
        driver.quit()
        return "Nothing found"
    retrieved_text = "Image occurs in: " + json.dumps(search_results[:max_items],ensure_ascii=False)
    search_log={original_post: retrieved_text}
    with open("logging/visual_search_results.json", 'a', encoding='utf-8') as f: 
        f.write(json.dumps(search_log, ensure_ascii=False, indent=4))

    return retrieved_text

def driver_quit():
    driver.quit()


# Unit test:
if __name__ =="__main__":
    pass
    # text="'cash backing to remake scotland a wastefree economy the cash is from the scottish institute for remanufacture supported by the government to create a wastefree circular economy remanufacturing is a process that takes old but highvalue products and restores them to an asnew condition'"
    # title="Scotland's Investment in Waste-Free Circular Economy"
    # questions=['Scottish Institute for Remanufacture government funding', 'Success stories of remanufacturing in Scotland']
    # get_evidence(text, title, questions)    
    # scraper("https://www.bbc.com/news/worl-us-canada-68244352", 2000)
    visual_search("twitter/Mediaeval2016_TestSet_Images/syrian_children_1.jpg","Syrian Girl who sells gum")