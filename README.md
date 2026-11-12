# 🛡️ Ping-Guard-Bot

Monitor autônomo de uptime em Python puro para vigiar APIs, sites, painéis e webhooks 24 horas por dia, enviando alertas instantâneos via **Discord** e **Telegram** sempre que um serviço sair do ar ou voltar a ficar online.

[![Powered by Raven Host](https://img.shields.io/badge/Powered%20by-Raven%20Host-7c3aed?style=for-the-badge&logo=icloud&logoColor=white)](https://raven-host-cloud.elementfx.com)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/Dependências-Zero%20(Stdlib)-10b981?style=for-the-badge)](#)

---

> 🚀 **Rodando e patrocinado com alta performance por [Raven Host](https://raven-host-cloud.elementfx.com)**  
> *Precisa manter este monitor ou seus bots de Discord, WhatsApp e Telegram rodando 24h na nuvem sem deixar o PC ligado? Hospede seu código em segundos na **☁ Raven Host** — infraestrutura otimizada para Python, Node.js e IA.*

---

## ✨ Recursos Principais

* **Zero Dependências Externas:** Utiliza apenas bibliotecas nativas do Python (`urllib`, `json`, `logging`). Não exige `pip install` nem ambientes virtuais pesados.
* **Alertas Inteligentes (Anti-Spam):** Notifica apenas na mudança de estado (quando o serviço **cai** e quando **volta**), evitando flood no seu chat.
* **Multi-Plataforma:** Suporte simultâneo para Webhooks do **Discord** e Bots do **Telegram**.
* **Ultra Leve:** Consome menos de 15MB de RAM, ideal para rodar em containers e servidores cloud enxutos.

---

## 📂 Estrutura do Projeto

```
text
ping-guard-bot/
├── config.json      # Lista de URLs monitoradas e tokens de alerta
├── ping_guard.py    # Script principal de monitoramento contínuo
└── README.md        # Documentação do projeto
```

## ⚙️ Instalação e Uso

1. Clone o repositório
```
git clone [https://github.com/SEU-USUARIO/ping-guard-bot.git](https://github.com/SEU-USUARIO/ping-guard-bot.git)
cd ping-guard-bot
```
2. Configure os alvos e alertas
Edite o arquivo config.json com os links que deseja vigiar e suas chaves de notificação (deixe em branco a plataforma que não for usar):
```
{
    "intervalo_segundos": 60,
    "telegram_token": "SEU_TOKEN_DO_BOT_TELEGRAM_AQUI",
    "telegram_chat_id": "SEU_CHAT_ID_AQUI",
    "discord_webhook_url": "SUA_WEBHOOK_URL_DO_DISCORD_AQUI",
    "alvos": [
        {
            "nome": "Meu Site Principal",
            "url": "[https://raven-host-cloud.elementfx.com](https://raven-host-cloud.elementfx.com)"
        },
        {
            "nome": "API do Meu Bot",
            "url": "[https://sua-api.com/health](https://sua-api.com/health)"
        }
    ]
}
```

