from flask import Flask, render_template, request, jsonify
import cohere, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
co = cohere.Client(os.getenv("COHERE_API_KEY"))
chat_history=[]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    user_message=request.json["message"]
    response=co.chat(model="command-r-plus", message=user_message, chat_history=chat_history)
    bot_reply=response.text
    chat_history.append({"role":"USER","message":user_message})
    chat_history.append({"role":"CHATBOT","message":bot_reply})
    return jsonify({"reply":bot_reply})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",5000)))
