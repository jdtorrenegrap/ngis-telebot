import requests
import logging
import os

# Crear la carpeta 'log' si no existe
log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configurar el logger para que registre en el archivo 'log/bot.log'
log_file = os.path.join(log_directory, 'bot.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP no exitosos
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching data from {url}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred while fetching data from {url}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred while fetching data from {url}: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred while fetching data from {url}: {req_err}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching data from {url}: {e}")
    return None