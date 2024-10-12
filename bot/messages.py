from analysis.data_analysis import analyze_trends, compare_sensors, sensor_analysis
from api.api import fetch_data
from bot.config import GET_ALERT, GET_READS
from telebot import TeleBot

def send_welcome(bot: TeleBot, message):
    welcome_message = (
        "Hola, soy Ngis, tu asistente. Para obtener información, utiliza los siguientes comandos:\n"
        "1. Obtener las últimas 5 lecturas:\n"
        "/consult\n"
        "2. Ver alertas configuradas:\n"
        "/alert\n"
        "3. Obtener información del sensor que más datos ha enviado:\n"
        "/get\n"
        "4. Tendencias temporales:\n"
        "/trend\n\n"
    )
    bot.reply_to(message, welcome_message)

def get_reads(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "Obteniendo las últimas 5 lecturas...")
    send_initial_message()

    reading_data = fetch_data(GET_READS)
    if reading_data:
        latest_readings = reading_data[-5:]
        result = "Últimos datos:\n\n"
        for i, reading in enumerate(latest_readings, 1):
            device_id = reading.get('device_id', 'N/A')
            unit_id = reading.get('unit_id', 'N/A')
            value = reading.get('value', 'N/A')
            created_at = reading.get('created_at', 'N/A')

            # Determinar la unidad basada en el tipo de sensor
            if 'temperature' in device_id.lower():
                value = f"{value} °C"
            elif 'humidity' in device_id.lower():
                value = f"{value} %"

            result += (
                f"Lectura {i}:\n"
                f"  - Sensor: {device_id}\n"
                f"  - Unidad: {unit_id}\n"
                f"  - Valor: {value}\n"
                f"  - Fecha: {created_at}\n\n"
            )
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ocurrió un error al obtener los datos.")

def get_alerts(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "Obteniendo alerta configurada...")
    send_initial_message()

    alert_data = fetch_data(GET_ALERT)
    if alert_data:
        latest_alert = alert_data
        result = "Alerta Configurada:\n\n"
        for i, alert in enumerate(latest_alert, 1):
            if isinstance(alert, list) and len(alert) >= 3:
                result += (
                    f"  - Temperatura: {alert[0]}°C\n"
                    f"  - Humedad: {alert[1]}%\n"
                    f"  - Humedad del suelo: {alert[2]}%\n\n"
                )
            else:
                result += f"Alerta:\n  - Dato no disponible\n\n"
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ocurrió un error al obtener la alerta.")

def get_sensor(bot: TeleBot, message): 
    send_initial_message = lambda: bot.reply_to(message, "Realizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result = sensor_analysis(data)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ocurrió un error al obtener el análisis.")

def get_trend(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "Realizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result =  analyze_trends(data)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ocurrió un error al obtener el análisis.")