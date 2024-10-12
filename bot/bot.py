from telebot import TeleBot
from bot.config import TOKEN
from bot.messages import get_sensor, get_trend, send_welcome, get_reads, get_alerts

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    send_welcome(bot, message)

@bot.message_handler(commands=['consult'])
def handle_consult(message):
    get_reads(bot, message)

@bot.message_handler(commands=['alert'])
def handle_alert(message):
    get_alerts(bot, message)

@bot.message_handler(commands=['get'])
def handle_get_sensor(message):
    get_sensor(bot, message)

@bot.message_handler(commands=['trend'])
def handle_get_trend(message):
    get_trend(bot, message)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, "No reconozco ese comando. Por favor, usa uno de los siguientes comandos:\n/start\n/consult\n/alert\n/obtener")

if __name__ == "__main__":
    bot.polling(none_stop=True)