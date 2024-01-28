import openai
import pandas as pd
from duckduckgo_search import DDGS
from openai import OpenAI
import os
import numpy as np
from config import prompts_root,imgbed_root
from selenium import webdriver
from time import sleep
import pyautogui
import html2text


openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
with open(prompts_root+'keyword_prompt.md', 'r', encoding='utf-8') as f:
        keyword_prompts = f.read()


def generate_keywords(text):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an professional in optimizing the keywords for search engine"},
            {"role": "user", "content": keyword_prompts + '\n' + text + '\nKeywords Output:\n'}
        ],
        temperature=0.1
    )
    response = completion.choices[0].message.content
    # return response
    keywords = response.replace("\n", " ").split(" ")
    if keywords[0] == "False":
        return "False"
    else:
        return " ".join(keywords[1:])

def create_embedding(text, engine="text-embedding-ada-002"):
        return client.embeddings.create(input=[text], model=engine).data[0].embedding

def preprocess(results,query):
    if results == None or results == []:
        print("No search result!")
        return None
    results = pd.DataFrame(results)
    results.columns = ['title', 'link', 'text']
    results['query'] = [query for _ in results.index]
    results['text_length'] = results['text'].str.len()
    results['ada_search'] = results['text'].apply(lambda x: create_embedding(x))
    return results

def find_top_similar_results(df: pd.DataFrame, query: str, n: int):
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    if len(df.index) < n:
        n = len(df.index)
    embedding = create_embedding(query)
    df1 = df.copy()
    df1["similarities"] = df1["ada_search"].apply(lambda x: cosine_similarity(x, embedding))
    best_results = df1.sort_values("similarities", ascending=False).head(n)
    return best_results.drop(['similarities', 'ada_search'], axis=1).drop_duplicates(subset=['text'])


def ddg_search(keywords, query, top_k=4):
    # query=ddg_translate(query, to = "en")["translated"]

    # Do the duckduckgo search
    with DDGS() as ddgs:
        search_results=list(ddgs.text(keywords, region='wt-wt', safesearch='off', timelimit='y', max_results=10))
        search_results=preprocess(search_results,query)
        if search_results is None: return None

    # Rank the results based on semantic similarity
    similar_results = find_top_similar_results(search_results, query, top_k)
    google_findings = similar_results['text'].to_list()
    links = similar_results['link'].to_list()
    return google_findings, links


def search_results_dump(google_findings, links):
    res_txt = ""
    for i, finding in enumerate(google_findings):
        res_txt += finding + f' [Source]({links[i]})'
    return res_txt


def text_search(text):
    keywords = generate_keywords(text)
    if keywords == "False":
        return None
    serach_results = ddg_search(keywords, text)
    if serach_results is None:
        return None
    google_findings, links = serach_results
    search_result_txt=search_results_dump(google_findings, links)
    return search_result_txt


def visual_search(source, chrome_driver_path = 'chromedriver.exe', is_url=True):

    # Find the chromederver suitable for your chrome version here: "http://npm.taobao.org/mirrors/chromedriver/"+version+"/chromedriver_win32.zip", https://googlechromelabs.github.io/chrome-for-testing/#stable

    # Initialize the Chrome webdriver and open the URL
    options = webdriver.ChromeOptions()
    # if is_url:
    #     options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    driver.get('https://www.google.com/imghp')
    sleep(1)  
    button = driver.find_element_by_css_selector("div.nDcEnd")
    button.click()
    sleep(1) 

    if is_url:
        # use the image url
        if "http" not in source: 
            source=imgbed_root+source
        driver.find_element_by_css_selector("input.cB9M7").send_keys(source)
        search_button=driver.find_element_by_css_selector("div.Qwbd3")
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
        upload_button = driver.find_element_by_css_selector("div.ZeVBtc>span")
        upload_button.click()

    sleep(2)
    results=driver.find_elements_by_css_selector("a")
    title_links=[]
    for result in results:
        # title = result.text
        link = result.get_attribute('href')
        if "google.com" in link:
            continue
        title=result.text
        title_link={"title":title,"link":link,"text":title}
        title_links.append(title_link)
    
    results
    driver.get(link)
    result=driver.find_elements_by_css_selector("body")[0]
    html=result.text
    text = html2text.html2text(html).replace("\n"," ")
    driver.quit()
    return text


if __name__ == '__main__':
    print(text_search('''Paying For His Crimes: As Part Of His Plea Bargain, Michael Flynn Is Visiting High Schools To Speak To Kids About Why They Shouldn’t Lie To The FBI About Contacts With Russian Diplomats http://clckhl.co/FQ1FMdO
Tradueix la publicació'''))
    # print(visual_search("https://th.bing.com/th/id/OIP.sbADfa_B4kN9odcQs3IWTwHaEK?w=268&h=180&c=7&r=0&o=5&dpr=1.1&pid=1.7"))
