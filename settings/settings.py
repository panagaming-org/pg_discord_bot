import json

async def get_settings_async():
    settings = {}
    with open("settings.json") as settings:
        settings = json.load(settings)   
    return settings

def get_settings():
    settings = {}
    with open("settings/settings.json") as settings:
        settings = json.load(settings)
    return settings


async def get_verified_role_id():
    settings = await get_settings_async()
    role_id = settings['discord']['roles']['member_role_id']
    return role_id

async def get_aislated_role_id():
    settings = await get_settings_async()
    role_id = settings['discord']['roles']['aislated_role_id']
    return role_id

async def get_guild_id():
    settings = await get_settings_async()
    guild_id = settings['discord']['server']['id']
    return guild_id

async def get_api_backend_async():
    settings = await get_settings_async()
    api_url = settings["backend_server"]
    return api_url

def get_api_backend():
    settings = get_settings()
    api_url = settings['backend_server']
    return api_url