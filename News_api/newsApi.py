import os
import requests
import json
import datetime
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
print("yesterday" , yesterday)
def get_news(term):
    if term == "AIML":
        term = "AI"
        url = ('https://newsapi.org/v2/everything?'
        f'q={"+".join(term.split())}+("AI" OR "ML" OR "artificial intelligence" OR "machine learning")&'
        f'from={yesterday}&'
        'searchIn=title,description&'
        'language=en&'
        'pageSize=20&'
        'sortBy=popularity&'
        'apiKey=7af83bf241d1457596a8e285a221b3ed')
    elif term == "AR-VR":
        date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        term = "AR"
        url = ('https://newsapi.org/v2/everything?'
        f'q={"+".join(term.split())}+("AR" AND "VR" OR "augmented reality" OR "virtual reality" OR "AR VR" OR "ARVR")&'
        f'from={date}&'
        'searchIn=title,description&'
        'language=en&'
        'pageSize=20&'
        'sortBy=popularity&'
        'apiKey=7af83bf241d1457596a8e285a221b3ed')
    else :
        date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        term = "blockChain"
        url = ('https://newsapi.org/v2/everything?'
        f'q={"+".join(term.split())}+("blockchain" OR "cryptocurrency" OR "bitcoin" OR "ethereum OR WEB3")&'
        f'from={date}&'
        'searchIn=title,description&'
        'sortBy=popularity&'
        'language=en&'
        'pageSize=20&'
        'apiKey=7af83bf241d1457596a8e285a221b3ed')
        
    responses = requests.get(url)
    return responses.json() 
