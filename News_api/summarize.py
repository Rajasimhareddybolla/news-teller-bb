from langchain_google_genai import ChatGoogleGenerativeAI
import datetime
import os
# from langchain_chroma.vectorstores import Chroma

from langchain.prompts import   PromptTemplate
from langchain.chains import LLMChain
import json
## adjust the prompt in this its not good

apis = ["AIzaSyCVD2lN4cUXiiR3B3uW4XqZQbPPsUxaT0Q" ,"AIzaSyDiGh-sgE-MqFVq-4fRELfji61e66WatrI" , "AIzaSyBrS_cbP7xSgblv0lJg9nbcdyN3SS8xl6g"  , "AIzaSyD6dV0eY_tTTyIYKVUuRdi4FYSyzsOktU0" , "AIzaSyDFb40ou0vHKAseJG50S1-Cmm_m5Oc1Q2k" , "AIzaSyB3r2h5-SrU60MyaZIXg-Dl7fuJ4fG-Oro" ,"AIzaSyCMd32WUqHQc0P5M3qw9m6lteBfAYbcS2I" , "AIzaSyBfKmCv0vO9HFzk3UpkqkRFRIQhPpfEyWU"]
import random
class NewsSummarizer:
    def __init__(self ):

        os.environ["GOOGLE_API_KEY"] = random.choice(apis)
        os.makedirs("text/summarization" , exist_ok = True)
        if not os.path.exists("text/summarization/history.json"):
            with open("text/summarization/history.json" , "w") as f:
                json.dump({"history":[]} , f)
        # self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    def summarize(self, urls ,query_news , query_edge):
        print("started")
        urls = sorted(urls)
        with open("text/summarization/history.json" , "r") as f:
            history_summarization = json.load(f)
        
        for i in history_summarization["history"]:
            if i["urls"] == urls:
                print("returning from history")
                path = i["path"]
                with open(path , "r") as f:
                    return f.read()
        # with open("db/history.json" , "r") as f:
        #     history = json.load(f)
        # found = False
        # for i in history["history"]:
        #     if i["urls"] == urls:
        #         urls = i["urls"]
        #         persistent_dir = i["storage"]   
        #         found = True
        #         break
        # if not found:
        #     persistent_dir = convert_db.convert_db(urls)
        
        # self.vdb = Chroma(persist_directory=persistent_dir, embedding_function=self.embedding)
        # Retrieve all documents from the vector database
        # Use MMR retriever to get diverse samples
        # retriever = self.vdb.as_retriever(search_type="mmr", search_kwargs={"k": 15 , "fetch_k":30 ,  "lambda_mult":0.24})
        # retriever_docs = retriever.get_relevant_documents("")
        retriever_docs = '\n \n'
        file_path_news = f"text/{datetime.datetime.now().strftime('%Y-%m-%d')}_{query_news}_{query_edge}.json"
        with open(file_path_news) as file:
            data = json.load(file)
            for article in data["Articles"]:
                if article["id"] in urls:
                    retriever_docs += f"Title: {article['title']}\n\nContent: {article['content']}\n\n [Source: {article['title']}, Author: {article['author']}]"

        summarization_prompt = PromptTemplate(
            input_variables=["context"],
            template=
            """
                You are an expert news analyst and summarizer. Your task is to create a comprehensive, well-structured summary based on the provided context. Follow these guidelines:

                1. Relevance Check:
                   - If the context contains relevant information, proceed with the summary.

                2. Summary Structure:
                   - Begin with a concise overview of the main topic or event.
                   - Organize the summary into clear sections, covering all major points from the context.
                   - Use bullet points or numbered lists for clarity when appropriate.

                3. Content Requirements:
                   - Provide a detailed, long-form summary that captures the essence of the information.
                   - Cover ALL topics mentioned in the context, prioritizing their importance and relevance.
                   - Include key facts, figures, quotes, and any significant developments or implications.
                   - Highlight any controversies, differing viewpoints, or areas of uncertainty.

                4. Context Enhancement:
                   - Supplement the summary with your expert knowledge to provide additional context or background information.
                   - Explain complex terms or concepts that may not be familiar to a general audience.

                5. Source Attribution:
                   - For each major point or piece of information, cite the source using the following format:
                     [Source: <source name>, Author: <author if available>]
                   - If an image is mentioned, include its description and source: [Image: <brief description>, Source: <source name>]

                6. Conclusion:
                   - End with a brief conclusion that summarizes the key takeaways or implications of the information.

                7. Metadata:
                   - After the summary, list all unique metadata entries found in the context, formatted as:
                     [Source: <source>, Image: <image URL>, Date: <date>, Heading: <heading>, Author: <author>]
                   - Include only available fields for each entry.

                Context:
                {context}

                Summary:
                """
        )
        summarize_chain = LLMChain(
            llm=self.model,
            prompt=summarization_prompt,
            verbose=True
        )
        os.makedirs("text/summarization" , exist_ok = True)
        path = f"text/summarization/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.txt"
        print(retriever_docs)
        summary = summarize_chain.run( context=retriever_docs)
        os.makedirs("text/summarization" , exist_ok=True)
        history_json = "text/summarization/history.json"
        with open(history_json , "r") as f:
            history = json.load(f)
        history["history"].append({"path":path , "urls":urls})
        with open(history_json , "w") as f:
            json.dump(history , f)
        with open(path, "w") as f:
            f.writelines(summary)

        return summary 

