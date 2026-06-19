import discord
from discord.ext import commands

async def warn_user_embed(points):
    embed = discord.Embed(
        title="Has enviado un enlace con contenido dañino.",
        description="En PanaGaming queda totalmente prohibido el envio de contenido de ese tipo.",
        color=discord.Color.red()
    )
    embed.add_field(
        name="Oportunidades",
        value=f"{points}",
        inline=False
    )
    return embed

