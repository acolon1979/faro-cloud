
import time
import requests

ENDPOINT_COMANDO = "https://faro-cloud.onrender.com/ultimo-comando"
COMANDO_FILE = "mensagens_gpt.txt"

ultimo_comando = ""

print("🔁 Faro Sync rodando... (Ctrl+C para sair)")

while True:
    try:
        response = requests.get(ENDPOINT_COMANDO)
        if response.status_code == 200:
            novo_comando = response.text.strip()
            if novo_comando and novo_comando != ultimo_comando:
                print(f"📥 Novo comando recebido: {novo_comando}")
                with open(COMANDO_FILE, "w") as f:
                    f.write(novo_comando)
                ultimo_comando = novo_comando
        else:
            print(f"⚠️ Erro ao acessar {ENDPOINT_COMANDO}: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    time.sleep(3)
