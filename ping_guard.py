# python ping_guard.py

'''
Como ele funciona (Explicação passo a passo para leigos):

    A Lista de Alvos: O script lê um arquivo de configuração onde você cadastra os links (APIs, sites ou webhooks) que deseja vigiar.

    A Ronda (O Ping): A cada intervalo de tempo determinado (por exemplo, a cada 5 minutos), o script faz um "toque" digital (uma requisição web) 
    em cada link da lista para ver se eles respondem com sucesso.

    O Diagnóstico:

        Se o site/bot responder normalmente, ele continua a ronda em silêncio.

        Se o link falhar, demorar demais ou retornar um erro (como o famoso erro 500 ou 404), o script entende que o serviço caiu.

    O Alerta Imediato: Assim que a queda é detectada, o script envia um aviso automático direto para o seu Telegram ou Discord (avisando que o serviço X ficou offline).

    Rodando 24h na Nuvem: Como ele foi feito para rodar direto sem desligar, você o hospeda em um servidor leve (como na Raven Host) e ele trabalha sozinho dia e noite para você.
'''

import time
import json
import urllib.request
import urllib.error
import urllib.parse
import logging
from datetime import datetime

# Configuração de logs organizados no terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

CONFIG_FILE = 'config.json'

def carregar_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar {CONFIG_FILE}: {e}")
        return None

def enviar_alerta_telegram(token, chat_id, mensagem):
    if not token or not chat_id or token == "SEU_TOKEN_DO_BOT_TELEGRAM_AQUI":
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        dados = urllib.parse.urlencode({'chat_id': chat_id, 'text': mensagem}).encode('utf-8')
        req = urllib.request.Request(url, data=dados, method='POST')
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        logging.error(f"Falha ao enviar alerta no Telegram: {e}")

def enviar_alerta_discord(webhook_url, mensagem):
    if not webhook_url or webhook_url == "SUA_WEBHOOK_URL_DO_DISCORD_AQUI":
        return
    try:
        dados = json.dumps({"content": mensagem}).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=dados, headers={'Content-Type': 'application/json'}, method='POST')
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        logging.error(f"Falha ao enviar alerta no Discord: {e}")

def disparar_alerta(config, mensagem_alerta):
    logging.warning(mensagem_alerta)
    enviar_alerta_telegram(
        config.get('telegram_token'), 
        config.get('telegram_chat_id'), 
        mensagem_alerta
    )
    enviar_alerta_discord(
        config.get('discord_webhook_url'), 
        mensagem_alerta
    )

def testar_url(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Ping-Guard-Bot/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as resposta:
            return 200 <= resposta.status < 400
    except urllib.error.HTTPError as e:
        logging.error(f"Erro HTTP {e.code} para {url}")
        return False
    except urllib.error.URLError as e:
        logging.error(f"Erro de URL/Conexão para {url}: {e.reason}")
        return False
    except Exception as e:
        logging.error(f"Erro inesperado para {url}: {e}")
        return False

def main():
    logging.info("🛡️ Ping-Guard-Bot iniciado com sucesso!")
    
    # Dicionário para controlar o estado anterior e evitar spam de alertas repetidos
    estados_anteriores = {}

    while True:
        config = carregar_config()
        if not config:
            time.sleep(10)
            continue

        intervalo = config.get('intervalo_segundos', 60)
        alvos = config.get('alvos', [])

        for alvo in alvos:
            nome = alvo.get('nome')
            url = alvo.get('url')

            status_atual = testar_url(url)
            estado_anterior = estados_anteriores.get(nome, True) # Assume que estava OK inicialmente

            if status_atual:
                logging.info(f"[ONLINE] {nome} ({url})")
                if not estado_anterior:
                    # O serviço voltou ao ar!
                    disparar_alerta(config, f"🟢 RECUPERADO: O serviço *{nome}* voltou a ficar ONLINE!")
                estados_anteriores[nome] = True
            else:
                logging.warning(f"[OFFLINE] {nome} ({url})")
                if estado_anterior:
                    # O serviço acabou de cair!
                    disparar_alerta(config, f"🚨 ALERTA DE QUEDA: O serviço *{nome}* ({url}) está OFFLINE!")
                estados_anteriores[nome] = False

        time.sleep(intervalo)

if __name__ == '__main__':
    main()
# CODE FIM.    