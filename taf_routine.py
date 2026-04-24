import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }, timeout=20)

if __name__ == "__main__":
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    message = f"""
<b>TAF Routine</b>

Routine eseguita.
Ora: {now}
""".strip()

    send_message(message)
