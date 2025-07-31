import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://faro-cloud.onrender.com/ultimo-comando"
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")

print("🎧 Faro Listener 2.2 rodando... (Ctrl+C para sair)")
print("🔍 Verificando variáveis de ambiente:")
print(f"  🟡 TRELLO_LIST_ID: {TRELLO_LIST_ID}")
print(f"  🟡 TRELLO_KEY: {TRELLO_KEY}")
print(f"  🟡 TRELLO_TOKEN: {TRELLO_TOKEN}")

# Verificação crítica
if not all([TRELLO_LIST_ID, TRELLO_KEY, TRELLO_TOKEN]):
    print("❌ ERRO: Uma ou mais variáveis de ambiente estão ausentes!")
    print("💡 Verifique se o arquivo .env está na mesma pasta e com as variáveis:")
    print("    TRELLO_KEY=...")
    print("    TRELLO_TOKEN=...")
    print("    TRELLO_LIST_ID=...")
    exit(1)

ultimo_comando = None

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            try:
                data = response.json()
                titulo = data.get("titulo", "").strip()
                descricao = data.get("descricao", "").strip()
                comando = f"{titulo}||{descricao}"

                if comando and comando != ultimo_comando and titulo:
                    print(f"📥 Novo comando do ChatGPT: {comando}")
                    ultimo_comando = comando

                    # Cria o card no Trello
                    url = "https://api.trello.com/1/cards"
                    query = {
                        "key": TRELLO_KEY,
                        "token": TRELLO_TOKEN,
                        "idList": TRELLO_LIST_ID,
                        "name": titulo,
                        "desc": descricao,
                    }
                    r = requests.post(url, params=query)
                    if r.status_code == 200:
                        print("✅ Card criado com sucesso!")
                    else:
                        print(f"❌ Erro ao criar card: {r.text}")
            except ValueError:
                print("⚠️ Resposta não formatada como JSON. Pulando...")
        else:
            print(f"⚠️ Erro ao acessar {API_URL}: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Erro geral: {e}")

    time.sleep(5)
