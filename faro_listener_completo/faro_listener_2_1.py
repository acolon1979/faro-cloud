
import os
import time
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_ID_LISTA = os.getenv("TRELLO_ID_LISTA")

API_URL = "https://faro-cloud.onrender.com/ultimo-comando"

ultimo_comando_processado = None

print("🎧 Faro Listener 2.1 rodando... (Ctrl+C para sair)")

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200 and response.text:
            try:
                data = response.json()
            except Exception:
                print("⚠️ Resposta não formatada como JSON. Pulando...")
                time.sleep(3)
                continue

            titulo = data.get("titulo", "").strip()
            descricao = data.get("descricao", "").strip()

            if titulo and descricao:
                comando_atual = f"{titulo} || {descricao}"
                if comando_atual != ultimo_comando_processado:
                    print(f"📥 Novo comando do ChatGPT: {comando_atual}")
                    url = "https://api.trello.com/1/cards"
                    query = {
                        "key": TRELLO_KEY,
                        "token": TRELLO_TOKEN,
                        "idList": TRELLO_ID_LISTA,
                        "name": titulo,
                        "desc": descricao,
                    }
                    response = requests.post(url, params=query)
                    if response.status_code == 200:
                        print("✅ Card criado com sucesso!")
                        ultimo_comando_processado = comando_atual
                    else:
                        print(f"❌ Erro ao criar card: {response.text}")
            else:
                print("⏳ Aguardando comando válido...")
        else:
            print(f"⚠️ Erro ao acessar {API_URL}: {response.status_code}")
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")
    time.sleep(3)
