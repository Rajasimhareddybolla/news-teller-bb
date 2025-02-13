from bs4 import BeautifulSoup
import json
import requests
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
embedding = GoogleGenerativeAIEmbeddings(model = "gemini-1.5-pro")

def get_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    heading = soup.find("h1").get_text()
    image = soup.find("img").get("src")
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_="content")
    context = main_content.get_text().replace("\n", "").replace("\t", "")
    
    content = {
        "heading": heading,
        "image": image,
        "content": context
    }
    
    return json.dumps(content, ensure_ascii=False, indent=2)