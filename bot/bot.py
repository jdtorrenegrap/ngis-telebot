import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from telebot import TeleBot, types
from bot.messages import get_analyze, get_sensor, get_trend, send_welcome, get_reads, get_alerts

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
TOKEN = os.getenv('TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Verificar que el token se haya cargado correctamente
if TOKEN is None:
    raise ValueError("El token del bot no se ha encontrado en las variables de entorno.")

bot = TeleBot(TOKEN)
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

@app.on_event("shutdown")
async def shutdown_event():
    bot.remove_webhook()

@app.post("/webhook")
async def webhook(request: Request):
    if request.headers.get('content-type') == 'application/json':
        json_str = await request.body()
        update = types.Update.de_json(json_str.decode('utf-8'))
        bot.process_new_updates([update])
        return {"status": "ok"}
    return {"status": "error"}

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

@bot.message_handler(commands=['analyze'])
def handle_get_analyze(message):
    get_analyze(bot, message)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message,
                 "👩‍🌾 Senda\nNo reconozco ese comando. Por favor, usa uno de los siguientes comandos:\n\n"
                 "1️⃣/consult\n"
                 "2️⃣/alert\n"
                 "3️⃣/get\n"
                 "4️⃣/trend\n"
                 "5️⃣/analyze\n"
                 )

@app.get("/validate")
def read_root():
    return {"message": "Bot corriendo"}