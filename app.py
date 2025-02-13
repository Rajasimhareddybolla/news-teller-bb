from flask import Flask, request, jsonify ,send_file
from flask_cors import CORS
from News_api.get_preview import get_info
from News_api.fetch_news import get_unified_news

import datetime
import json
import os
from News_api.summarize import NewsSummarizer
from News_api.chat_with_ai import Chat
from News_api.txt_2_speech import text_to_speech
import destroy

summarizer = NewsSummarizer()
app = Flask(__name__)

chats_count = 0
global_chat = Chat()
no = 30
CORS(app, resources={r"/*": {"origins": "*"}})
print("hell i am executed")
@app.route("/get_preview", methods=["GET"])
def get_preview():

    url = request.args.get("url")
    print(url)
    url = url.split(",")
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    print("url == ",url)
    content = get_info(url[0])
    return content
@app.route("/change_articles")
def change_articles():
    no_change  = request.args.get("no")
    global no
    no = no_change
    return jsonify({"response":"sucesses"})
@app.route("/delete" , methods = ["POST"])
def delete():
    if request.method == "POST":
        with open("db/last_run_date.txt" , "w") as file:
            file.write("")
        
    return jsonify({"response":"sucess"})      
    

@app.route("/get_daily_news" , methods = ["GET","POST"])
def get_daily_news():
    destroy.destroy()
    print("get_daily_news")
    if request.method == "POST":
        data = request.get_json()
        query_news = data.get("query_news")
        query_edge = data.get("query_edge")
    else:
        query_news = request.args.get("query_news")
        query_edge = request.args.get("query_edge")
    
    if query_news is None or query_edge is None:
        return jsonify({"error": "Missing query parameters"}), 400
    os.makedirs("text", exist_ok=True)
    file_path = f"text/{datetime.datetime.now().strftime('%Y-%m-%d')}_{query_news}_{query_edge}.json"
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path , "r") as f:
            print("file exists")
            return jsonify(json.load(f))
    response_news  = get_unified_news(query_news , query_edge , no)
    print("response_news")
    with open(file_path , "w") as f:
        json.dump(response_news , f , indent=4)
    return jsonify(response_news)

@app.route("/summarize" , methods = ["GET" , "POST"])
def summarize():
    print("summarize")
    if request.method == "POST":
        id = request.json.get("urls")
    else:
        id = request.args.get("urls")
    id = id.split(',')
    print("urls = ",id)
    print(id)
    for i in range(len(id)):
        id[i] = int(id[i])


    if not id:
        return jsonify({"error": "Text parameter is missing"}), 400
    summary = summarizer.summarize(id , "ml" , "aiml")
    summary = {"summary":summary}
    return jsonify(summary)


# Initialize global variables


@app.route("/continue_chat", methods=["GET", "POST"])
def continue_chat():
    """Continue an ongoing chat session."""
    try:
        if request.method == "POST":
            data = request.get_json()
        else:  
            data = request.args.to_dict()

        # Validate chat_id parameter
        chat_id = data.get("chat_id")
        print("chat_id" , chat_id)
        if not chat_id and chat_id != 0:
            return jsonify({"error": "Chat ID parameter is missing"}), 400
        try:
            chat_id = int(chat_id)
        except ValueError:
            return jsonify({"error": "Chat ID must be an integer"}), 401
        
        # Validate text parameter
        text = data.get("text")

        if not text:
            return jsonify({"error": "Text parameter is missing"}), 402
        print("text:", text)

        # Retrieve chat instance
        chat_instance = Chat.get_chat_instance(chat_id)
        print("chat_instance:", chat_instance)

        # Generate AI response
        response = chat_instance.chat_with_ai(text)
        print("AI response:", response)

        # Save chat history
        chat_instance.save_chat_instance(chat_id)
        print("Chat instance saved")

        final_response = {"response": response}
        print("Sending response:", final_response)
        return jsonify(final_response)

    except Exception as e:
        print(f"Error in continue_chat: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/chat", methods=["GET", "POST"])
def chat():
    """Initialize a new chat session."""
    global chats_count
    
    if request.method == "POST":
        data = request.get_json()
    else:  # GET request
        data = request.args.to_dict()
    
    # Validate URLs parameter
    urls = data.get("urls")
    if not urls:
        return jsonify({"error": "URLs parameter is missing"}), 400
    
    try:
        # Parse URLs into a sorted list of integers
        urls = sorted([int(url.strip())  for url in urls.split(",")])
    except ValueError:
        return jsonify({"error": "Invalid URLs format, must be comma-separated integers"}), 400

    # Generate new chat ID
    chat_id = chats_count
    chats_count += 1

    # Create chat instance
    try:
        chat_instance = global_chat.get_chat_instance(chat_id=chat_id, urls=urls)
    except Exception as e:
        return jsonify({"error": f"Failed to create chat instance: {e}"}), 500
    print(chat_instance)
    return jsonify({"response": "Success", "chat_id": chat_instance})
@app.route("/get_audio" , methods = ["GET" ,"POST"])
def conversation_gen():
    print("audio generator")
    if request.method == "POST":
        id = request.json.get("urls")
    else:
        id = request.args.get("urls")
    print("ids =", id)
    if not id:
        return jsonify({"error": "Text parameter is missing"}), 400
    output_folder = "summarized/audio"
    path = text_to_speech(id, output_folder)
    print("done generated audio at =", path)
    return send_file(path, mimetype='audio/mpeg')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

