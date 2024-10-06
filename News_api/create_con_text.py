import os
import json

import glob

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
# from langchain_chroma.vectorstores import Chroma
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, PromptTemplate
from langchain.chains import LLMChain
import random
apis = ["AIzaSyCVD2lN4cUXiiR3B3uW4XqZQbPPsUxaT0Q" ,"AIzaSyDiGh-sgE-MqFVq-4fRELfji61e66WatrI" , "AIzaSyBrS_cbP7xSgblv0lJg9nbcdyN3SS8xl6g"  , "AIzaSyD6dV0eY_tTTyIYKVUuRdi4FYSyzsOktU0" , "AIzaSyDFb40ou0vHKAseJG50S1-Cmm_m5Oc1Q2k" , "AIzaSyB3r2h5-SrU60MyaZIXg-Dl7fuJ4fG-Oro" ,"AIzaSyCMd32WUqHQc0P5M3qw9m6lteBfAYbcS2I" , "AIzaSyBfKmCv0vO9HFzk3UpkqkRFRIQhPpfEyWU"]

class NewsSummarizer:
    def __init__(self, model_name):
        os.environ["GOOGLE_API_KEY"] = random.choice(apis)

        self.model = ChatGoogleGenerativeAI(model=model_name)
        self.summarization_prompt = self.create_prompt_template()

    def extract_json(self ,text):
        f_place = text.find("{")
        l_place = text.rfind("}")
        if f_place == -1 or l_place == -1:
            return None  # No JSON object found
        return text[f_place:l_place+1]
    def create_prompt_template(self):
        return PromptTemplate(
            input_variables=["context", "query"],
            template="""
                You are tasked with generating a professional conversation based on the provided context. Create a detailed dialogue between two experts: Andrew Krepthy (PhD, Tesla) and Smithi (Researcher at Google DeepMind).
                Please provide only a JSON object, nothing more and nothing less.
                The conversation should:
                1. Be long enough to create a minimum 25 interactions dialogue when spoken.
                2. Cover all the major topics provided in the context.
                3. Demonstrate deep technical knowledge and insights from both participants.
                4. Include discussions on potential implications, challenges, and future directions of the mentioned topics.
                5. Be formatted as a JSON object with alternating speakers.

                Context: {context}

                Query: {query}
                
                Answer:
                Provide the conversation in the following JSON format:
                {{
                    "conversation": [
                        {{
                            "speaker": "Andrew Krepthy"(one of the seniour AI experts and tecnology enthustiast from Stanford University and worked in tesla ,openai and currently working in google),
                            "text": "..."
                        }},
                        {{
                            "speaker": "Smithi"(researcher at google deepmind and also a tech enthusiaist who loves to read and discuss about the latest tecnology and AI),
                            "text": "..."
                        }},
                        // ... (continue alternating speakers for a 10 minute conversation)
                    ]
                }}

                Ensure the conversation is substantive, technically accurate, and reflects the expertise of both speakers on the topics provided in the context.
                You are allowed to use your knowledge to generate the conversation and you should cover all the topics which were given in the context (high priority).
                Additionally, if you find any relevant sources or metadata in the context, include them at the end of the JSON object like this:
                "sources": [
                    {{
                        "title": "...",
                        "url": "...",
                        "date": "..."
                    }}
                ]
                (Include only available fields)
                """
        )

    # def retrieve_documents(self, query):
    #     return self.retriever.invoke(query)

    # def prepare_docs_string(self, retriever_docs):
    #     return "\n\n".join([f"Document {i+1}:\n{doc.page_content}\n\n Metadata: {doc.metadata}\n" for i, doc in enumerate(retriever_docs)])

    def summarize(self, query, context):
        summarize_chain = LLMChain(
            llm=self.model,
            prompt=self.summarization_prompt,
            verbose=True
        )
        return summarize_chain.run(query=query, context=context)

    def save_summary(self, summary, file_path):
        with open(file_path, "w") as f:
            # Extract JSON string
            json_string = self.extract_json(summary)
            # Convert JSON string to Python dictionary
            json_obj = json.loads(json_string)
            # Write the dictionary to the file with indentation
            json.dump(json_obj, f, indent=4)
        return True

    def run(self, ids , context_path, output_file):
        with open(context_path , "r") as f:
            context = json.load(f)
        doc = []
        print(context)
        for article in context["Articles"]:
            if article["id"] in ids:
                doc.append(article["content"])

        summary = self.summarize(query="cover most of the content . and must provide in json format", context='\n'.join(doc))

        self.save_summary(summary, output_file)

def get_most_recent_file(base_path):
    files = [f for f in glob.glob(os.path.join(base_path, '*')) if os.path.isfile(f)]
    if not files:
        print(f"No files found in {base_path}")
        return None
    most_recent_file = max(files, key=os.path.getmtime)
    print(f"Most recent file: {most_recent_file}")
    return most_recent_file

def get_context( urls , output_file):
    summarizer = NewsSummarizer(
        model_name="gemini-1.5-pro",

    )
    
    summarizer.run(urls, get_most_recent_file("text"), output_file)
    return output_file


