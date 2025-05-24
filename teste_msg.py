import requests

WHAPI_TOKEN = "g8KttsB9TAh62aG4orRdacyYbITYwkHg"
CHAT_ID = "558188711106"  # ou ID do grupo, como "1203...@g.us"
MENSAGEM = "✅ Agora sim! Enviado com endpoint /api/messages/text"

def enviar_mensagem(chat_id, mensagem):
    url = "https://gate.whapi.cloud/api/messages/text"
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    payload = {
        "to": chat_id,
        "body": mensagem
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        print("✅ Mensagem enviada com sucesso!")
        print("📨 Resposta:", response.json())
    except requests.RequestException as e:
        print("❌ Erro ao enviar mensagem:", e)

if __name__ == "__main__":
    enviar_mensagem(CHAT_ID, MENSAGEM)
