import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN non trovato")
    if not CHAT_ID:
        raise ValueError("CHAT_ID non trovato")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        },
        timeout=20
    )

    print("Telegram status:", response.status_code)
    print("Telegram response:", response.text)

    response.raise_for_status()

if __name__ == "__main__":
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    message = f"""
<b>TAF Routine</b>

Routine eseguita correttamente.
Ora: {now}
""".strip()

    send_message(message)
