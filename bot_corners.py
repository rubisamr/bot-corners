import os
import requests
import time

# Obtener credenciales desde variables de entorno
TELEGRAM_TOKEN = os.getenv("7859598111:AAFT2gqd6YELtz5ZpSxPEXrFSziYGfeE3gs")
TELEGRAM_CHAT_ID = os.getenv("1483987781")

# URL de la API (debes reemplazarla con la API real que usas)
API_URL = "https://www.bet365.pe/#/IP/B1"

def enviar_mensaje_telegram(mensaje):
    """Envía un mensaje a Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    requests.post(url, data=data)

def analizar_partidos():
    """Consulta la API y filtra partidos con 2 o menos córners entre el minuto 15 y 30."""
    try:
        response = requests.get(API_URL)
        partidos = response.json()  # ⚠️ Adapta esto según la estructura de tu API
        
        for partido in partidos:
            minuto = partido["minuto"]  # ⚠️ Verifica cómo se llama este dato en tu API
            corners = partido["corners_1T"]  # ⚠️ Verifica cómo se llama este dato en tu API
            
            if 15 <= minuto <= 30 and corners <= 2:
                mensaje = f"⚽ Partido {partido['equipo_local']} vs {partido['equipo_visitante']}\n" \
                          f"📍 Minuto: {minuto}\n" \
                          f"🔹 Córners en 1T: {corners}\n" \
                          f"🔔 Posible oportunidad para apostar a córners en 1T"
                enviar_mensaje_telegram(mensaje)
                print(f"🔔 Notificación enviada: {mensaje}")

    except Exception as e:
        print(f"⚠️ Error en la API: {e}")
        enviar_mensaje_telegram(f"⚠️ Error en el bot de córners: {e}")

# Ejecutar cada 5 minutos (opcional)
while True:
    analizar_partidos()
    time.sleep(300)  # Esperar 5 minutos antes de la siguiente consulta
