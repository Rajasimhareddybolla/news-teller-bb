import os
import json
from dotenv import load_dotenv
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from . import convert_db  # assuming this is your local utility module

# Chiat class managing instances and interactions with the FAISS index and LLM
import random
class Chat:
    instances = {}
    instances_urls = {}
    def __init__(self, urls=None):
        apis = ["AIzaSyCVD2lN4cUXiiR3B3uW4XqZQbPPsUxaT0Q" ,"AIzaSyDiGh-sgE-MqFVq-4fRELfji61e66WatrI" , "AIzaSyBrS_cbP7xSgblv0lJg9nbcdyN3SS8xl6g"  , "AIzaSyD6dV0eY_tTTyIYKVUuRdi4FYSyzsOktU0" , "AIzaSyDFb40ou0vHKAseJG50S1-Cmm_m5Oc1Q2k" , "AIzaSyB3r2h5-SrU60MyaZIXg-Dl7fuJ4fG-Oro" ,"AIzaSyCMd32WUqHQc0P5M3qw9m6lteBfAYbcS2I" , "AIzaSyBfKmCv0vO9HFzk3UpkqkRFRIQhPpfEyWU"]
        if urls:
            os.environ["GOOGLE_API_KEY"] = random.choice(apis)
            self.conversation_history = []
            os.makedirs("chats", exist_ok=True)
            if not os.path.exists("chats/history.json"):
                with open("chats/history.json", "w") as f:
                    json.dump({"history": []}, f)

            with open("chats/history.json", "r") as f:
                history = json.load(f)

            found = False
            for entry in history["history"]:
                if entry["urls"] == urls:
                    persistent_dir = entry["storage"]
                    found = True
                    break

            if not found:
                persistent_dir = convert_db.convert_db(urls)

            # Initialize embeddings and retriever
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


            new_vector_store = FAISS.load_local(
                persistent_dir, self.embeddings, allow_dangerous_deserialization=True
            )
            self.retriever = new_vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 10})
            # Initialize LLM and prompt system
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

            system_prompt = (
                "You are a friendly assistant for chat tasks. "
                "Use retrieved context to answer questions briefly, "
                "if you dont know the answer and not in context , provide a relevant response . "
                " you can use your creative and communication skills. If no context matches, use your own knowledge."
                "example: "
                "user : hai , content : bla bla bla (not useful)"
                "assistent: hello i am a friendly assistant , how can i help you today ?"
                "in this case let the answer should be relevent and general"
            )

            self.prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{input}, context: {context}"),
                ]
            )

            self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
            self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    @classmethod
    def get_chat_instance(cls, chat_id, urls=None):
        print("urls:", urls)
        print("chat_id:", chat_id)
        print("instances:", cls.instances)

        # Return existing instance if already created
        if chat_id in cls.instances:
            return cls.instances[chat_id]

        if urls is None:
            raise ValueError("URLs must be provided for new chat instances")

        urls_str = ','.join(str(url) for url in urls)
        if urls_str in cls.instances_urls:
            return cls.instances_urls[urls_str]

        # Create a new instance if not found
        instance = Chat(urls=urls)
        cls.instances[chat_id] = instance
        cls.instances_urls[urls_str] = chat_id
        return chat_id

    def save_chat_instance(self, chat_id):
        os.makedirs("chats", exist_ok=True)
        with open(f"chats/{chat_id}.json", "w") as f:
            json.dump(self.conversation_history, f)

    def chat_with_ai(self, user_input):
        if user_input.lower() == 'quit':
            return self.conversation_history

        # Retrieve documents from FAISS and run through RAG chain
        retrieved_docs = self.retriever.invoke(user_input)        
        self.conversation_history.append(f"Human: {user_input}, Retrieved Docs: {retrieved_docs}")

        response = self.rag_chain.invoke({"input": user_input})
        ai_response = response["answer"]
        print(f"AI: {ai_response}")

        self.conversation_history.append(f"AI: {ai_response}")
        return ai_response