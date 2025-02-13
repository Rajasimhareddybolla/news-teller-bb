


import os 

import requests
from dotenv import load_dotenv
import json
load_dotenv()
def get_news(query):
    ## query= ai research papers , ml , .....
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
    search_url = "https://api.bing.microsoft.com/v7.0/search"

    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt  , "responseFilter" :"Webpages"}
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }


    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()

        print("Headers:")
        print(response.headers)

        print("JSON Response:")

    except Exception as ex:
        raise ex
    return response.json() 