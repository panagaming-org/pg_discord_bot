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
import utils.url_utils as url_utils
import controller.user_warn_controller as user_warn_controller

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

user_history = {}

# Configuración
FLOOD_THRESHOLD = 5      # Máximo de mensajes permitidos
FLOOD_WINDOW = 3         # Segundos en los que ocurre el flood
FLOOD_BAN_REASON = "Detección automática de Flood"

dotenv.load_dotenv()
TOKEN = os.getenv('token')

async def get_user_by_id(guild, id_user):
    user = await guild.fetch_member(id_user)
    return user

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
    
async def ban_user(user, guild, reason="No especificada"):
    try:
        await guild.ban(user, reason=reason, delete_message_seconds=604800)
    except discord.Forbidden:
        print(f"❌ Error: El bot no tiene permisos de 'Banear Miembros' o el usuario tiene un rol superior.")
    except discord.HTTPException as e:
        print(f"❌ Error de Discord al intentar banear: {e}")

async def verify_message(message) -> bool:
    valid = True
    if await scan.message_with_link(message):
        link_list = await scan.links_from_message(message)
        for link in link_list:
            if await scan.is_server_spam(link):
                valid = False
                break
            domain = await url_utils.extract_domain(link)
            if await scan.is_banned_link(domain):
                valid = False
                break
    return valid

async def delete_message(message):
    await message.delete()

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    user_id = message.author.id
    now = datetime.datetime.now()

    message_content = message.content
    guild = message.guild

    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append(now)
    user_history[user_id] = [t for t in user_history[user_id] if (now - t).total_seconds() < FLOOD_WINDOW]

    if len(user_history[user_id]) > FLOOD_THRESHOLD:
        user = await get_user_by_id(guild, user_id)
        if not await user_has_any_role(user):
            await ban_user(user, guild, FLOOD_BAN_REASON)
            return
        
        await block_user(user)
        return
    
    if not await verify_message(message_content):
        user = await get_user_by_id(guild, user_id)
        if not await user_has_any_role(user):
            await ban_user(user, guild, reason="Has empezado a hacer Spam nada más unirte.")
            return
        
        await user_warn_controller.rest_user_points(user_id)
        if await user_warn_controller.user_without_points(user_id):
            await ban_user(user, guild, reason="Has estando enviando enlaces y/o contenido inapropiado despues de ser avisado 3.")
            return

if __name__ == "__main__":
    database.initialice_db()
    database.reaload_database()
    bot.run(TOKEN)