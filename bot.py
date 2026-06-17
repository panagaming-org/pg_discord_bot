import discord
from discord.ext import commands, tasks
from discord.utils import *
import dotenv
import os
import datetime
import json
import controller.scan_controller as scan
import utils.list_utils as list_utils
import instance.database as database
import settings.settings as settings

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

async def get_user_by_id(id_user):
    user = bot.fetch_user(id_user)
    return user

async def get_guild():
    guild_id = await settings.get_guild_id()
    guild = bot.get_guild(guild_id)
    return guild

async def get_role_by_id(role_id):
    guild_id = await settings.get_guild_id()
    
    guild = bot.get_guild(guild_id)
    if guild is None:
        print(f"❌ No se pudo encontrar el servidor con ID {guild_id}")
        return None

    role = guild.get_role(role_id)
    return role

async def user_has_any_role(user) -> bool:
    return len(user.roles) > 1

async def block_user(user):
    block_role_id = await settings.get_aislated_role_id()
    role = await get_role_by_id(block_role_id)
    if role in None:
        print("No se ha encontrado el role de bloquear usuarios.")
        return
    try:
        await user.add_role(role)
    except discord.Forbidden:
        print("❌ El bot no tiene permisos suficientes para asignar este rol (Jerarquía).")
    except discord.HTTPException as e:
        print(f"❌ Error al conectar con Discord: {e}")
    
async def ban_user(user, reason="No especificada"):
    guild = await get_guild()

    try:
        await guild.ban(user, reason=reason, delete_message_seconds=604800)
    except discord.Forbidden:
        print(f"❌ Error: El bot no tiene permisos de 'Banear Miembros' o el usuario tiene un rol superior.")
    except discord.HTTPException as e:
        print(f"❌ Error de Discord al intentar banear: {e}")

async def verify_message(message) -> bool:
    valid = True
    # Se comprueba si el mensaje tiene un enlace o no.
    if scan.message_with_link(message):
        # Extrae los enlaces.
        link_list = scan.links_from_message(message)
        
        for link in link_list:
            if scan.is_server_spam(link):
                valid = False
                break
            if scan.is_banned_link(link):
                valid = False
                break
    return valid

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
        if not user_has_any_role(user):
            print("Usuario no verificado, porcedemos a banear!")
            await ban_user(user)
            return
        
        await block_user(user)
        return
    
    if not verify_message(message):
        user = await get_user_by_id(user_id)
        if not user_has_any_role(user):
            await ban_user(user, reason="Has empezado a hacer Spam nada más unirte.")
            return

    await bot.process_commands(message)

if __name__ == "__main__":
    database.initialice_db()
    bot.run(TOKEN)