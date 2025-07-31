from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Pega as chaves da API do Trello via variáveis de ambiente
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

@app.route('/set-comando', methods=['POST'])
def set_comando():
    titulo = request.json.get("titulo", "").strip()
    descricao = request.json.get("descricao", "").strip()
    comando = f"{titulo}||{descricao}"
    
    with open("comando_atual.txt", "w") as f:
        f.write(comando)

    return jsonify({"status": "comando recebido", "comando": comando})

@app.route('/ultimo-comando', methods=['GET'])
def get_ultimo_comando():
    try:
        with open("comando_atual.txt", "r") as f:
            comando = f.read().strip()
        if "||" in comando:
            titulo, descricao = comando.split("||", 1)
            return jsonify({
                "titulo": titulo.strip(),
                "descricao": descricao.strip()
            })
        else:
            return jsonify({})
    except FileNotFoundError:
        return jsonify({})

if __name__ == '__main__':
    print("⚡ Faro Cloud rodando no Render!")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
