import pandas as pd
import requests
from datetime import datetime, timedelta
import time

# Configurações da Whapi.cloud
WHAPI_INSTANCE_ID = "SEU_INSTANCE_ID"
WHAPI_TOKEN = "SEU_TOKEN"
PLANTAO_GROUP_ID = "ID_DO_GRUPO_PLANTAO@g.us"
RECEPCAO_GROUP_ID = "ID_DO_GRUPO_RECEPCAO@g.us"
ARQUIVO_ESCALA = "Escala_Maio_2025.xlsx"


def enviar_mensagem(grupo_id, mensagem):
    url = f"https://gate.whapi.cloud/message/text?instance_id={WHAPI_INSTANCE_ID}&token={WHAPI_TOKEN}"
    payload = {
        "to": grupo_id,
        "text": mensagem
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Mensagem enviada com sucesso para {grupo_id}")
    except requests.RequestException as e:
        print(f"Erro ao enviar mensagem para {grupo_id}: {e}")


def montar_mensagem(df, data, turno):
    plantonistas = df[(df["data"] == data) & (df["turno"] == turno)]
    nomes = ", ".join(plantonistas["nome"].fillna("Vaga livre").tolist())
    mensagem = f"📋 Plantão {turno.capitalize()} de {data.strftime('%d/%m/%Y')}:\n\n{nomes}"
    return mensagem


def rotina_envio():
    hoje = datetime.now().date()
    hora = datetime.now().hour

    try:
        df = pd.read_excel(ARQUIVO_ESCALA)
        df["data"] = pd.to_datetime(df["data"], dayfirst=True).dt.date
        df["turno"] = df["turno"].str.lower()
    except Exception as e:
        print(f"Erro ao ler a escala: {e}")
        return

    # Envio 6 dias antes ou 1 dia antes
    turnos_futuros = df[(df["data"] - hoje).isin([timedelta(days=6), timedelta(days=1)])]

    for data_plantao, turno in turnos_futuros[["data", "turno"]].drop_duplicates().values:
        mensagem = montar_mensagem(df, data_plantao, turno)
        enviar_mensagem(PLANTAO_GROUP_ID, mensagem)

    # Envio no dia, no início do turno
    turnos_hoje = df[df["data"] == hoje]["turno"].unique()

    for turno in turnos_hoje:
        if (hora == 6 and turno == "manhã") or (hora == 12 and turno == "tarde") or (hora == 18 and turno == "noite"):
            mensagem = montar_mensagem(df, hoje, turno)
            enviar_mensagem(RECEPCAO_GROUP_ID, mensagem)


if __name__ == "__main__":
    while True:
        rotina_envio()
        time.sleep(3600)  # roda a cada 1 hora
