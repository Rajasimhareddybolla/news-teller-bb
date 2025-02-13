import os
from uuid import uuid4
from langchain.docstore import InMemoryDocstore
import json
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import datetime
import faiss
from langchain.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import glob

load_dotenv()
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
splitter = RecursiveCharacterTextSplitter(chunk_overlap=150, chunk_size=600)

# Function to get the most recent file
def get_most_recent_file(base_path):
    files = [f for f in glob.glob(os.path.join(base_path, '*')) if os.path.isfile(f)]
    if not files:
        print(f"No files found in {base_path}")
        return None
    most_recent_file = max(files, key=os.path.getmtime)
    print(f"Most recent file: {most_recent_file}")
    return most_recent_file

# Function to convert documents to FAISS index
def convert_db(urls, persist_directory=None):
    print("urls=  == = =", urls)
    texts = []

    # Read the most recent JSON file containing article history
    with open(get_most_recent_file("text")) as f:
        history = json.load(f)

    # Iterate through articles and collect the ones specified in `urls`
    for article in history["Articles"]:
        if article["id"] in urls:
            # Debugging: Print the type and content of article["brief"] and article["content"]
            print(f"article['brief'] type: {type(article['brief'])}, ")
            print(f"article['content'] type: {type(article['content'])},")

            chunks = splitter.split_text(article["brief"] + article["content"])
            print(len(article['brief'] + article['content']))
            # Debugging: Print the output of split_text
            print(f"split_text output: {chunks}")

            for chunk in chunks:
                print(article["id"], "  i am chunk")
                chunk = Document(page_content=chunk, metadata={"source": article["urls"], "heading": article["title"]})
                texts.append(chunk)
    # Create a directory for storing the FAISS index
    os.makedirs("db", exist_ok=True)
    if not persist_directory:
        persist_directory = f"db/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"

    print(texts, persist_directory)

    index = faiss.IndexFlatL2(len(embedding.embed_query("hello world")))
    vector_store = FAISS(embedding_function=embedding, index=index, docstore=InMemoryDocstore({}) , index_to_docstore_id={})
    uuids = [str(uuid4()) for _ in range(len(texts))]
    vector_store.add_documents(documents=texts, ids=uuids)
    vector_store.save_local(persist_directory)
    return persist_directory
    # for url in urls:
    #     print("done")
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.content , 'html.parser')
    #     haeding = soup.find("h1").get_text()
    #     image = soup.find("img").get("src")
    #     author = soup.find("a" , class_ = "author")
    #     if not author:
    #         author = "Unknown"
    #     else:
    #         author = author.get_text()
    #     main_content = soup.find('main') or soup.find('article') or soup.find('div' , class_ = "content")
    #     chunks = splitter.split_text(main_content.get_text(strip=True))
    #     for chunk in chunks:
    #         chunk = Document(page_content=chunk, metadata={"source": url, "heading": haeding , "image": image , "author": author})
    #         texts.append(chunk)