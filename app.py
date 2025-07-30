from flask import Flask, request, jsonify
from pyngrok import ngrok
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

@app.route('/')
def index():
    return "Faro Cloud webhook rodando!"

@app.route('/criar-card', methods=['POST'])
def criar_card():
    data = request.json
    url = "https://api.trello.com/1/cards"
    query = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "idList": data.get("idList"),
        "name": data.get("name"),
        "desc": data.get("desc", ""),
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        return jsonify({"status": "success", "card": response.json()})
    else:
        return jsonify({"status": "error", "message": response.text}), response.status_code

if __name__ == '__main__':
    public_url = ngrok.connect(5000, "http")
    print(f"⚡ Webhook disponível em: {public_url}")
    app.run(host='0.0.0.0', port=5000)
