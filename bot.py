import discord
from discord.ext import commands, tasks
from discord.utils import *
import dotenv
import os
import datetime

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

USER_ROLE_ID = 1239939068905914368
MEMBER_ROLE_ID = 852500184662409216
STAFF_ROLE_ID = 856835937816674314
EJECUTIVE_ROLE_ID = 889578160495140898

user_history = {}

# Configuración
FLOOD_THRESHOLD = 5      # Máximo de mensajes permitidos
FLOOD_WINDOW = 3         # Segundos en los que ocurre el flood
BAN_REASON = "Detección automática de Flood"


dotenv.load_dotenv()
TOKEN = os.getenv('token')


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
        print("Usuario {} ha superado el límite de mensajes.".format(message.author))
    
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)