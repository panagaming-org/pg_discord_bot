import model.dao.user_warn_dao as user_warn_dao

async def create_user_warn(id_user):
    await user_warn_dao.add_user_warn(id_user, 3)

async def get_by_user_id(id_user):
    return await user_warn_dao.get_by_user_id(id_user)

async def rest_user_points(id_user):
    warn_user = await user_warn_dao.get_by_user_id(id_user)
    if not warn_user:
        await create_user_warn(id_user)
    else:
        await user_warn_dao.update_warn(
            id_user = id_user,
            points = warn_user.points - 1
        )

async def user_without_points(id_user) -> bool:
    return await user_warn_dao.warn_without_points(id_user)