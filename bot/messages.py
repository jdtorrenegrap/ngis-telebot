import os
from dotenv import load_dotenv
from analysis.data_analysis import analyze_trends, compare_sensors, latest_readings, sensor_analysis
from api.api import fetch_data
from telebot import TeleBot

load_dotenv()
GET_READS = os.getenv('GET_READS')
GET_ALERT = os.getenv('GET_ALERT')
KNOW = os.getenv('KNOW')

def send_welcome(bot: TeleBot, message):
    
    welcome_message = (
        "👩‍🌾¡Hola! Soy Senda, tu asistente. Para obtener información sobre el sistema Ngis, utiliza estos comandos fáciles:\n\n"
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
        f"Para más información sobre los análisis realizados por Senda, haz clic {KNOW}\n\n"   
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
        f"Para más información sobre los análisis realizados por Senda, haz clic {KNOW}\n\n"
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
                f"- Dispositivo: {reading['device_id']}\n"
                f"- Unidad: {reading['unit_id']}\n"
                f"- Valor: {reading['value']}\n"
                f"- Fecha: {reading['created_at']}\n\n"
            )
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "👩‍🌾 Senda\nOcurrió un error al obtener los datos.")
    send_option(bot, message)

def get_alerts(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nObteniendo alerta configurada...")
    send_initial_message()

    alert_data = fetch_data(GET_ALERT)
    if alert_data:
        latest_alert = alert_data
        result = "👩‍🌾 Senda\nAlerta Configurada:\n\n"
        for alert in latest_alert:
            if isinstance(alert, list) and len(alert) >= 3: #verifico si es una lista y si la longitud es al menos 3
                result += (
                    f"  - Temperatura: mayor a {alert[0]}°C\n"
                    f"  - Humedad: mayor a {alert[1]}%\n"
                    f"  - Humedad del suelo: menor a {alert[2]}%\n\n"
                )
            else:
                result += "👩‍🌾 Senda\nAlerta:\n  - Dato no disponible\n\n"
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "👩‍🌾 Senda\nOcurrió un error al obtener la alerta.")
    send_option(bot, message)

def get_sensor(bot: TeleBot, message): 
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nRealizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result = sensor_analysis(data)
        bot.reply_to(message,result)
    else:
        bot.reply_to(message, "👩‍🌾 Senda\nOcurrió un error al obtener el análisis.")
    send_option(bot, message)

def get_trend(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nRealizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result =  analyze_trends(data)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ocurrió un error al obtener el análisis.")
    send_option(bot, message)

def get_analyze(bot: TeleBot, message):
    send_initial_message = lambda: bot.reply_to(message, "👩‍🌾 Senda\nRealizando análisis...")
    send_initial_message()

    data = fetch_data(GET_READS)
    if data:
        result = compare_sensors(data)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Ocurrió un error al obtener el análisis.")
    send_option(bot, message)