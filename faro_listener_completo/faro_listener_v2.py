
import time
import requests
import os

COMANDO_FILE = "mensagens_gpt.txt"
API_URL = "https://faro-cloud.onrender.com/criar-card"
ID_LISTA_BACKLOG = "5c66fb8a6515a1188c7724b1"

def ler_comando():
    try:
        with open(COMANDO_FILE, "r") as file:
            linhas = file.readlines()
            if linhas:
                linha = linhas[0].strip()
                return linha
    except FileNotFoundError:
        return ""
    return ""

def limpar_comando():
    with open(COMANDO_FILE, "w") as file:
        file.write("")

def criar_card(titulo, descricao):
    payload = {
        "idList": ID_LISTA_BACKLOG,
        "name": titulo,
        "desc": descricao
    }
    response = requests.post(API_URL, json=payload)
    return response.status_code == 200

print("🎧 Faro Listener 2.0 rodando... (Ctrl+C para sair)")

ultimo_comando = ""

while True:
    comando = ler_comando()
    if comando and comando != ultimo_comando:
        print(f"📥 Novo comando do ChatGPT: {comando}")
        if "||" in comando:
            partes = comando.split("||")
            titulo = partes[0].strip()
            descricao = partes[1].strip()
            sucesso = criar_card(titulo, descricao)
            if sucesso:
                print("✅ Card criado com sucesso!")
                limpar_comando()
            else:
                print("❌ Erro ao criar card.")
        else:
            print("⚠️ Formato inválido. Esperado: TÍTULO || DESCRIÇÃO")
        ultimo_comando = comando
    time.sleep(3)
