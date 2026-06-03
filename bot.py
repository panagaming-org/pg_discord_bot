import discord
from discord.ext import commands, tasks
from discord.utils import *
import dotenv
import os
import datetime
import json
import controller.actions_controller as actions
import controller.scan_controller as scan

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

user_history = {}

# Configuración
FLOOD_THRESHOLD = 5      # Máximo de mensajes permitidos
FLOOD_WINDOW = 3         # Segundos en los que ocurre el flood
BAN_REASON = "Detección automática de Flood"

dotenv.load_dotenv()
TOKEN = os.getenv('token')

settings = {}
with open("settings.json") as settings:
    settings = json.load(settings)

async def get_user_by_id(id_user):
    user = bot.fetch_user(id_user)
    return user

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    user_id = message.author.id
    now = datetime.datetime.now()

    if user_id not in user_history:
        user_history[user_id] = []

    # Añadir timestamp actual y limpiar antiguos fuera de la ventana
    user_history[user_id].append(now)
    user_history[user_id] = [t for t in user_history[user_id] if (now - t).total_seconds() < FLOOD_WINDOW]

    # Verificar si excede el límite
    if len(user_history[user_id]) > FLOOD_THRESHOLD:
        user = await get_user_by_id(user_id)
        if scan.is_user_verified(user):
            print("Usuario no verificado, porcedemos a banear!")
        else:
            actions.block_user(user)
    
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)