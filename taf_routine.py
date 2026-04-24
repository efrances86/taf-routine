import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Aeroporto Venezia Tessera (LIPZ)
LAT = 45.5053
LON = 12.3519

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current_weather": True,
        "hourly": "relativehumidity_2m,pressure_msl,visibility,cloudcover",
        "timezone": "Europe/Rome"
    }

    r = requests.get(url, params=params, timeout=20)
    data = r.json()

    current = data["current_weather"]
    hourly = data["hourly"]

    return {
        "wind": round(current["windspeed"]),
        "wind_dir": current["winddirection"],
        "temp": round(current["temperature"]),
        "humidity": hourly["relativehumidity_2m"][0],
        "pressure": round(hourly["pressure_msl"][0]),
        "visibility": int(hourly["visibility"][0] / 1000),  # metri → km
        "cloud": hourly["cloudcover"][0]
    }

def wind_direction_it(deg):
    dirs = ["nord", "nord-est", "est", "sud-est", "sud", "sud-ovest", "ovest", "nord-ovest"]
    return dirs[int((deg + 22.5) / 45) % 8]

def cloud_description(cloud):
    if cloud < 20:
        return "nessuna nube inferiore a 1500 m e nessun cumulonembo"
    elif cloud < 50:
        return "poco nuvoloso"
    elif cloud < 80:
        return "parzialmente nuvoloso"
    else:
        return "molto nuvoloso"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    }, timeout=20)

if __name__ == "__main__":
    w = get_weather()
    now = datetime.utcnow().strftime("%H:%M UTC")

    message = f"""
Aeroporto di Venezia-Tessera

Osservazione

Il bollettino è stato emesso alle {now}

Vento {w['wind']} kt da {wind_direction_it(w['wind_dir'])}
Temperatura {w['temp']}°C
Umidità {w['humidity']}%
Pressione {w['pressure']} hPa
Visibilità {w['visibility']} km o più
{cloud_description(w['cloud'])}
""".strip()

    send_message(message)
