import requests
import telegram_secrets


def send_telegram_alert(message):
    bot_token = telegram_secrets.telegram_bot_token
    chat_id = telegram_secrets.telegram_chat_id

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("For some reason I can not sent the Telegram message.\nError.")
