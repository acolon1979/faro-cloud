from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Pega as chaves da API do Trello via variáveis de ambiente
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

# Armazena o último comando enviado (em memória)
ultimo_comando = ""

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

@app.route('/set-comando', methods=['POST'])
def set_comando():
    global ultimo_comando
    data = request.get_json()
    ultimo_comando = data.get("comando", "")
    return jsonify({"status": "comando recebido", "comando": ultimo_comando})

@app.route('/ultimo-comando', methods=['GET'])
def get_ultimo_comando():
    return ultimo_comando, 200

if __name__ == '__main__':
    print("⚡ Faro Cloud rodando no Render!")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
