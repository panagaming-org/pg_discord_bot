import os
import sys
import asyncio
import dotenv

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

dotenv.load_dotenv()
TOKEN = os.getenv('token_test')


@bot.command()
async def test_flood(ctx, cantidad: int = 10):
    for i in range(cantidad):
        await ctx.send(f"🔥 Mensaje de ataque {i + 1}")
        # Un micro-retraso para que los mensajes lleguen en ráfaga 
        # pero procesables por tu bot de seguridad
        await asyncio.sleep(0.1)

@bot.command()
async def test_raid_attack(ctx, *, mensaje: str = "¡Aviso importante! [Enlace: http://ejemplo.com]"):
    await ctx.send("🚨 Iniciando simulación de RAID en todos los canales...")

    tasks = []
    # Iteramos por todos los canales del servidor (guild)
    for canal in ctx.guild.text_channels:
        # Verificamos que el bot tenga permiso para enviar mensajes en ese canal
        if canal.permissions_for(ctx.guild.me).send_messages:
            tasks.append(canal.send(f"⚠️ **RAID TEST** ⚠️\n{mensaje}"))

    if not tasks:
        return await ctx.send("❌ No encontré canales donde tenga permisos para escribir.")

    # Ejecutamos el envío masivo
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send(f"✅ Simulación finalizada. Se intentó enviar a {len(tasks)} canales.")    
    

bot.run(TOKEN)
    
