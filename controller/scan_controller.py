import os
import discord
from discord.ext import commands

REGEX_SPAM = r"/(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite|t\.me|telegram\.me|chat\.whatsapp\.com)\/[a-zA-Z0-9-]{3,}/gi"
REGEX_LINK = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/\S*)?"

async def links_from_message(message):
    links = []
    for word in message.content.split():
        if re.match(REGEX_LINK, word):
            links.append(word)
    return links

async def links_allowed(links):
    for link in links:
        if is_banned_link(link):
            return False
        if is_server_spam(link):
            return False
        return True

async def message_with_link(message):
    if re.search(REGEX_LINK, message.content):
        return True 
    return False

async def is_server_spam(message):
    if re.search(REGEX_SPAM, message.content):
        return True
    return False

async def is_banned_link(message):
    return False  # Devuelve True si el mensaje contiene un enlace prohibido, de lo contrario False