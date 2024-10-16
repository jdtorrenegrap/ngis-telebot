import os
from dotenv import load_dotenv
from analysis.data_analysis import analyze_trends, compare_sensors, latest_readings, sensor_analysis
from api.api import fetch_data
from telebot import TeleBot

load_dotenv()
GET_READS = os.getenv('GET_READS')
GET_ALERT = os.getenv('GET_ALERT')
KNOW= os.getenv('KNOW')

def send_welcome(bot: TeleBot, message):
    
    welcome_message = (
                "👩‍🌾¡Hola! Soy Senda, tu asistente. Para obtener información sobre el sistema Ngis, utiliza estos comandos:\n\n"
                "1️⃣ Consultar lecturas de sensores:\n"
                "/consult\n"
                "2️⃣ Revisar alertas configuradas:\n"
                "/alert\n"
                "3️⃣ Obtener información de sensores:\n"
                "/get\n"
                "4️⃣ Obtener tendencias de datos:\n"
                "/trend\n"
                "5️⃣ Realizar análisis de datos:\n"
                "/analyze\n"
                f"📊 Más detalles sobre los análisis realizados por Senda {KNOW}\n\n"
    )
    bot.reply_to(message, welcome_message, parse_mode = "Markdown")

def send_option(bot: TeleBot, message):
    options_message = (
        "👩‍🌾 Senda\nOperación completada. Aquí tienes las opciones disponibles:\n\n"
       "1. Obtener las últimas lecturas:\n"
        "/consult\n"
        "2. Ver alertas configuradas:\n"
        "/alert\n"
        "3. Descubre información del sensor que más datos ha enviado:\n"
        "/get\n"
        "4. Analiza tendencias temporales:\n"
        "/trend\n"
        "5. Analiza datos de los sensores:\n"
        "/analyze\n"
        f"Más detalles sobre los análisis realizados por Senda aquí:{KNOW}\n\n"
    )
    bot.reply_to(message, options_message, parse_mode = "Markdown")

def get_reads(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nObteniendo la última lectura de cada dispositivo...")
    send_initial_message()

    reading_data = fetch_data(GET_READS)
    if reading_data:
        latest_readings_data = latest_readings(reading_data)

        result = "👩‍🌾 Senda\nDatos obtenidos:\n\n"
        for _, reading in latest_readings_data.iterrows():
            result += (
                f"Dispositivo: {reading['device_id']}\n"
                f" ⚙️Unidad: {reading['unit_id']}\n"
                f" 🔢Valor: {reading['value']}\n"
                f" 📅Fecha: {reading['created_at']}\n\n"
            )
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "👩‍🌾 ¡Ups! Parece que hubo un pequeño error al obtener los datos.")

def get_alerts(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nObteniendo alerta configurada...")
    send_initial_message()

    alert_data = fetch_data(GET_ALERT)
    if alert_data:
        result = "👩‍🌾 Senda\nAlertas Configuradas:\n\n"

        threshold_map={
            1:">",
            2:"<",
            3:"="
        }

        def get_threshold_operator(threshold_id):
            return threshold_map.get(threshold_id, "N/A")
        
        for alert in alert_data:
            if isinstance(alert, dict):  # Verifico si es un diccionario
                temperature = alert.get("temperature", "Dato no disponible")
                air_humidity = alert.get("air_humidity", "Dato no disponible")
                soil_humidity = alert.get("soil_humidity", "Dato no disponible")
                temperature_threshold_id = alert.get("temperature_threshold_id", "Dato no disponible")
                air_humidity_threshold_id = alert.get("air_humidity_threshold_id", "Dato no disponible")
                soil_humidity_threshold_id =  alert.get("soil_humidity_threshold_id", "Dato no disponible")
                
                temperature_threshold = get_threshold_operator(temperature_threshold_id)
                air_humidity_threshold = get_threshold_operator(air_humidity_threshold_id)
                soil_humidity_threshold = get_threshold_operator(soil_humidity_threshold_id)
 
                result += (
                    f" 🌡️Temperatura: {temperature_threshold}{temperature}°C\n"
                    f" 💧Humedad: {air_humidity_threshold}{air_humidity}%\n"
                    f" 🌱Humedad del suelo: {soil_humidity_threshold}{soil_humidity}%\n\n"
                )
            else:
                result += "👩‍🌾 Senda\nAlerta:\n  - Dato no disponible\n\n"
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "👩‍🌾 Senda\nOcurrió un error al obtener la alerta.")

def get_sensor(bot: TeleBot, message): 
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nRealizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result = sensor_analysis(data)
        bot.reply_to(message,result)
    else:
        bot.reply_to(message, "👩‍🌾 ¡Ups! Parece que hubo un pequeño error al obtener el análisis.")

def get_trend(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nRealizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result =  analyze_trends(data)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "👩‍🌾 ¡Ups! Parece que hubo un pequeño error al obtener el análisis.")

def get_analyze(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nRealizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result = compare_sensors(data)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "👩‍🌾 ¡Ups! Parece que hubo un pequeño error al obtener el análisis.")