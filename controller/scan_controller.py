import os
import re
import discord
from discord.ext import commands
import settings.settings as settings
import utils.list_utils as list_utils
import model.dao.banned_domain_dao as banned_domain_dao

REGEX_SPAM = r"/(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite|t\.me|telegram\.me|chat\.whatsapp\.com)\/[a-zA-Z0-9-]{3,}/gi"
REGEX_LINK = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/\S*)?"

'''
VALIDACION DE ENLACES ENVIADOS
'''

async def message_with_links(message):
    has_link = False
    list_words = list_utils.from_text_to_list(message)
    for word in list_words:
        if re.match(REGEX_LINK, word):
            has_link = True
            break
    return has_link

async def links_from_message(message):
    links = []
    for word in message.split():
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
    if re.search(REGEX_LINK, message):
        return True 
    return False

async def is_server_spam(message):
    if re.search(REGEX_SPAM, message):
        return True
    return False

async def is_banned_link(domain) -> bool:
    banned = False
    if await banned_domain_dao.get_by_domain(domain):
        banned = True
    return banned