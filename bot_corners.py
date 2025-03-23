import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configurar Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")  # Ruta en Render

def send_telegram_message(message):
    """Envía una notificación a Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logging.info("Notificación enviada a Telegram")
        else:
            logging.error(f"Error enviando mensaje: {response.text}")
    except Exception as e:
        logging.error(f"Error de conexión con Telegram: {e}")

def scrape_bet365():
    """Extrae datos en vivo de Bet365 usando Selenium."""
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.bet365.pe/#/IP/B1")
    time.sleep(5)  # Esperar a que cargue la página

    partidos = driver.find_elements(By.CLASS_NAME, "some-match-class")  # Ajusta esto
    for partido in partidos:
        try:
            minuto = int(partido.find_element(By.CLASS_NAME, "match-minute-class").text.replace("'", ""))
            corners = int(partido.find_element(By.CLASS_NAME, "corner-count-class").text)
            
            if 15 <= minuto <= 30 and corners < 2:
                mensaje = f"📢 Partido en vivo cumple condiciones: {partido.text}"
                send_telegram_message(mensaje)
                logging.info(mensaje)
        except Exception as e:
            logging.warning(f"No se pudo extraer datos de un partido: {e}")
    
    driver.quit()

def main():
    while True:
        logging.info("Iniciando revisión de partidos...")
        scrape_bet365()
        logging.info("Esperando 5 minutos antes de la siguiente verificación...")
        time.sleep(300)  # Revisar cada 5 minutos

if __name__ == "__main__":
    main()
