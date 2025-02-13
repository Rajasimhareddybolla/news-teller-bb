import os
import urllib.parse

import requests
import json
import datetime
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
print("yesterday" , yesterday)
def get_news(term , no):
    if term == "AIML":
        term = "AI"
        url = (f"https://newsapi.org/v2/everything?"
            f"q={'+'.join(term.split())}+(\"AI\" OR \"ML\" OR \"artificial intelligence\" OR \"machine learning\")&"
            f"from={yesterday}&to={yesterday}&"  # Ensuring the 'to' parameter is included
            "searchIn=title,description&"
            "language=en&"
            f"pageSize={no}&"
            "sortBy=popularity&"
            "apiKey=0173d015ce034b3482008b59a0f649d8")  # Ensure it's a properly formatted string
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
        'apiKey=0173d015ce034b3482008b59a0f649d8')
    else :
        date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        term = "blockChain"
        query = f'({urllib.parse.quote("blockchain OR cryptocurrency OR bitcoin OR ethereum OR WEB3")})'
        url = (
            f'https://newsapi.org/v2/everything?'
            f'q={"+".join(term.split())}+{query}&'
            f'from={date}&'
            'searchIn=title,description&'
            'sortBy=popularity&'
            'language=en&'
            'pageSize=20&'
            'apiKey=0173d015ce034b3482008b59a0f649d8'
        )
        
    responses = requests.get(url)
    return responses.json() 
