import os
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cargar variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configurar Selenium con opciones adecuadas para entornos sin interfaz gráfica
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicializar el WebDriver correctamente
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def send_telegram_message(message):
    """Envía una notificación a Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Lanza un error si la respuesta HTTP no es exitosa
        logging.info("✅ Notificación enviada a Telegram")
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error enviando mensaje a Telegram: {e}")

def scrape_bet365():
    """Extrae datos en vivo de Bet365 usando Selenium."""
    try:
        logging.info("🔍 Accediendo a Bet365...")
        driver.get("https://www.bet365.pe/#/IP/B1")
        time.sleep(5)  # Esperar a que la página cargue

        # Buscar los partidos en vivo (ajustar clases según la web)
        partidos = driver.find_elements(By.CLASS_NAME, "some-match-class")
        for partido in partidos:
            try:
                minuto = int(partido.find_element(By.CLASS_NAME, "match-minute-class").text.replace("'", ""))
                corners = int(partido.find_element(By.CLASS_NAME, "corner-count-class").text)

                if 15 <= minuto <= 30 and corners < 2:
                    mensaje = f"📢 Partido en vivo cumple condiciones: {partido.text}"
                    send_telegram_message(mensaje)
                    logging.info(mensaje)
            except Exception as e:
                logging.warning(f"⚠️ No se pudo extraer datos de un partido: {e}")

    except Exception as e:
        logging.error(f"❌ Error al acceder a Bet365: {e}")

def main():
    try:
        while True:
            logging.info("♻️ Iniciando revisión de partidos...")
            scrape_bet365()
            logging.info("⏳ Esperando 5 minutos antes de la siguiente verificación...")
            time.sleep(300)  # Revisar cada 5 minutos
    except KeyboardInterrupt:
        logging.info("🚪 Programa terminado por el usuario")
    finally:
        driver.quit()  # Asegurar que el WebDriver se cierra al salir

if __name__ == "__main__":
    main()
