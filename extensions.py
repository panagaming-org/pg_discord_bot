import json

async def get_settings():
    settings = {}
    with open("settings.json") as settings:
        settings = json.load(settings)   
    return settings

async def get_verified_role_id():
    settings = await get_settings()
    role_id = settings['discord']['member_role_id']
    return role_id

async def get_aislated_role_id():
    settings = await get_settings()
    role_id = settings['discord']['aislated_role_id']
    return role_id