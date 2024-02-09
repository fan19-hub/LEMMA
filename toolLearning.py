import openai
import re
import os
import json
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
from langdetect import detect
from openai import OpenAI
from config import prompts_root,imgbed_root
from time import sleep
# import html2text
from utils import predict_region

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()



def soure_filter(results):
    if results == None or results == []:
        return []
    for result in results:
        link=result['href']
        domain = re.search('https?://([A-Za-z_0-9.-]+).*', link).group(1)
        if domain in ["","www.facebook.com","m.facebook.com","www.reddit.com","www.weibo.com","twitter.com","www.tiktok.com","www.instagram.com","www.youtube.com","www.pinterest.com","www.linkedin.com","www.tumblr.com","www.douban.com","www.taobao.com","www.jd.com","www.amazon.com","www.ebay.com","www.aliexpress.com","www.bilibili.com","www.netflix.com","www.hulu.com","www.imdb.com","www.dailymotion.com","www.douyin.com","steamcommunity.com","m.ixigua.com"]:   
            results.remove(result)
    return results



def topic_relevance_filter(text, title, all_results, top_k, query_set, cutoff_index=200):
    # Structure flattern
    all_results_flatterned = []
    for qid, query in enumerate(all_results.keys()):
        results= all_results[query]
        for i,result in enumerate(results):
            id = qid*top_k + i        # we can use id/top_k to determine which query it belongs
            all_results_flatterned.append({id:result})

    # Prompt formation
    text=f"[title]:{title}\n{text[:cutoff_index]}"
    with open(prompts_root+'topic_relevance_filter.md', 'r', encoding='utf-8') as f: 
        prompt=f.read()
    prompt=prompt.format(TEXT=text, SEARCH_RESULT=json.dumps(all_results_flatterned))

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
        print("Tool learning Warning: Invalid response from topic_relevance_filter. Remain unchanged.")
        return results
    
    # Wash the string keys to int
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
        if relevance_labels[id]==1:
            qid=id//top_k
            query=query_set[qid]
            try:
                all_filtered_results[query].append(result)
            except:
                all_filtered_results[query]=[result]
    return all_filtered_results




def text_search(query, query_type="title", top_k=5):
    # Prefix
    region = predict_region(query)
    if detect(query) == 'zh-cn': prefix = '谣言 '
    else: prefix = 'fake news '
    if query_type=='title':
        query = prefix + query

    # DuckDuckGo Search
    max_results = 2*top_k
    with DDGS() as ddgs:
        try:
            results=list(ddgs.text(query, 
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
    


def evidence_retreival(text, title, questions, max_len=2000):
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
    all_search_results = topic_relevance_filter(text, title,  all_search_results, top_k, query_set)
    return json.dumps(all_search_results)



if __name__ =="__main__":
    text="'cash backing to remake scotland a wastefree economy the cash is from the scottish institute for remanufacture supported by the government to create a wastefree circular economy remanufacturing is a process that takes old but highvalue products and restores them to an asnew condition'"
    title="Scotland's Investment in Waste-Free Circular Economy"
    questions=['Scottish Institute for Remanufacture government funding', 'Success stories of remanufacturing in Scotland']
    evidence_retreival(text, title, questions)
    









# Appendix:

# import pyautogui
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# # def find_top_similar_results(results,query, top_k=2):
#     def create_embedding(text, engine="text-embedding-ada-002"):
#         return client.embeddings.create(input=[text], model=engine).data[0].embedding

#     if results == None or results == []:
#         print("No search result!")
#         return None
#     results=soure_filter(results)
#     results = pd.DataFrame(results)
#     results.columns = ['title', 'link', 'text']
#     results['query'] = [query for _ in results.index]
#     results['text_length'] = results['text'].str.len()
#     results['ada_search'] = results['text'].apply(lambda x: create_embedding(x))
#     def cosine_similarity(a, b):
#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
#     if len(results.index) < top_k:
#         top_k = len(results.index)
#     embedding = create_embedding(query)
#     df1 = results.copy()
#     df1["similarities"] = df1["ada_search"].apply(lambda x: cosine_similarity(x, embedding))
#     best_results = df1.sort_values("similarities", ascending=False).head(top_k)
#     similar_results=best_results.drop(['similarities', 'ada_search'], axis=1).drop_duplicates(subset=['text'])
#     google_findings = similar_results['text'].to_list()
#     links = similar_results['link'].to_list()
#     return (google_findings, links)


# def visual_search(source,text, chrome_driver_path = 'chromedriver.exe', is_url=True):

#     # Find the chromederver suitable for your chrome version here: "http://npm.taobao.org/mirrors/chromedriver/"+version+"/chromedriver_win32.zip", https://googlechromelabs.github.io/chrome-for-testing/#stable

#     # Initialize the Chrome webdriver and open the URL
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     service = ChromeService(executable_path=chrome_driver_path)
#     driver = webdriver.Chrome(service=service, options=options)


#     # Google Image Search Page
#     driver.get('https://www.google.com/imghp')
#     sleep(1)  
#     button = driver.find_element(By.CSS_SELECTOR, "div.nDcEnd")
#     button.click()
#     sleep(1) 

#     # Get the image
#     if is_url:
#         # use the image url
#         if "http" not in source: 
#             source=imgbed_root+source
#         driver.find_element(By.CSS_SELECTOR, "input.cB9M7").send_keys(source)
#         search_button=driver.find_element(By.CSS_SELECTOR, "div.Qwbd3")
#         search_button.click()       
#     else:
#         # upload the image
#         image_path=os.path.abspath(source) 
#         pyautogui.typewrite(image_path)
#         sleep(3)  
#         pyautogui.press('enter')
#         pyautogui.press('enter')
#         sleep(5)  
#         driver.find_element_by_name('file').send_keys(r"D:\test\xuexi\test\14.png")
#         upload_button = driver.find_element(By.CSS_SELECTOR, "div.ZeVBtc>span")
#         upload_button.click()

#     sleep(1)
#     # image serach result page
#     exact_search=driver.find_element(By.CSS_SELECTOR, "div.ICt2Q")
#     exact_search.click()
#     sleep(1)

#     # exact search result page
#     results=driver.find_elements(By.CSS_SELECTOR, "a")
#     search_results=[]
#     for result in results:
#         link = result.get_attribute('href')
#         if "google.com" in link:
#             continue
#         title=result.text
#         if title !="":
#             search_result={"title":title,"href":link,"text":title}
#             search_results.append(search_result)
#     if search_results==[]:
#         driver.quit()
#         return None
    
#     # Choose the top k websites that this image appears
#     top_k=10
#     driver.set_page_load_timeout(5)
#     image_source_titles, image_source_links=find_top_similar_results(search_results, text,top_k)
#     search_results_dump_txt=""
#     for title, link in zip(image_source_titles,image_source_links):
#         title=title.replace("\n"," ")
#         search_results_dump_txt+=f"[Title] {title}\n[Source] {link}\n"

#     driver.quit()
#     return search_results_dump_txt


# with open(prompts_root+'keyword_prompt.md', 'r', encoding='utf-8') as f:
#         keyword_prompts = f.read()


# def generate_keywords(text):
#     completion = client.chat.completions.create(
#         model="gpt-4-1106-preview",
#         # model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system",
#              "content": "You are an professional in optimizing the keywords for search engine"},
#             {"role": "user", "content": keyword_prompts + '\n' + text + '\nKeywords Output:\n'}
#         ],
#         temperature=0.1
#     )
#     response = completion.choices[0].message.content
#     # return response
#     keywords = response.replace("\n", " ").split(" ")
#     if keywords[0] == "False":
#         return "False"
#     else:
#         return " ".join(keywords[1:])

    # source_content_txt=""
    # max_len=500
    # for title, link in zip(image_source_titles,image_source_links):
    #     try:
    #         driver.get(link)
    #     except Exception as e:
    #         print(e)
    #         result=driver.find_element_by_css_selector("body")[0]
    #         html=result.text
    #         body_text=html2text.html2text(html).replace("\n"," ")[:max_len]
    #         source_content_txt += f"[Title] {title}\n[Text] {body_text} [Source] {link}\n"
