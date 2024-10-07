
import re


from . import newsApi

import requests
from bs4 import BeautifulSoup
def get_unified_news(query_news = None, query_edge = None):
    # response_edge = newsEdge.get_news(query_edge)
    id = 0 
    final = {"Articles":[]}
    # os.makedirs('daily_news', exist_ok=True)
    # file = f"daily_news/{datetime.datetime.now().strftime('%Y-%m-%d')}.json"
    # if os.path.exists(file):
    #     with open(file, "r") as f:
    #         final = json.load(f)
    #     return final , file
    # Convert response_edge forma
    # print(response_edge.keys())
    # for   article in response_edge["webPages"]["value"]:
    #     temp = {}
    #     temp['id'] = id + 1
    #     temp['title'] = article["name"]
    #     temp["brief"] = article["snippet"]
    #     temp['image'] = "https://cdn.vox-cdn.com/thumbor/a1UuqmTXeWu_sDyVAVipeGpIQ0s=/0x0:2040x1360/1200x628/filters:focal(1020x680:1021x681)/cdn.vox-cdn.com/uploads/chorus_asset/file/24016885/STK093_Google_04.jpg",
    #     temp['content'] = article["snippet"]
    #     temp['label'] = "AI_ML"
    #     temp["link"]  = article["url"]
    #     final["aritcles"].append(temp)
    # Convert response_news format
    news= ["AIML" , "Block Chain"]
    for i in range(len(news)):
        print("compiling")
        response_news = newsApi.get_news(news[i])
        for  article in response_news["articles"]:
            
            temp = {}
            temp["id"] = id
            temp["urls"] = article["url"]
            temp["title"] = article["title"]
            temp["brief"] = article["description"]
            temp["image"] =  article["urlToImage"]
            temp["content"] = fetch_full_content(article["url"])
            temp["label"] = news[i]
            if article["author"] is None:
                temp["author"] = "Anonymous"
            else:
                temp["author"] = article["author"]

            final["Articles"].append(temp)
            id +=1
    print("compiled")
    # file = f"daily_news/{datetime.datetime.now().strftime('%Y-%m-%d')}.json"
    # with open(file, "w") as f:
    #     json.dump(final, f  , indent=4)

    return final 
import requests
from bs4 import BeautifulSoup

def fetch_full_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all(['p', 'rem', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    content = []
    for tag in tags:
        if tag.name == 'p':
            content.append(f"{tag.text}\n")
        elif tag.name == 'rem':
            content.append(f"{tag.text}\n")
        elif tag.name.startswith('h'):
            level = int(tag.name[1])
            content.append(f"{'#' * level} {tag.text}\n")
    
    return ''.join(content)
