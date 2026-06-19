from sqlite3 import IntegrityError
from model.entity.UserWarn import UserWarn
import sqlalchemy

from instance.database import db

async def get_by_id(id):
    user_warn = db.query(UserWarn).filter(UserWarn.id == id).first()
    return user_warn

async def get_by_user_id(id_user):
    user_warn = db.query(UserWarn).filter(UserWarn.id_user == id_user).first()
    return user_warn

async def add_user_warn(user_id, points):
    try:
        user_warn = UserWarn(
            id_user=user_id,
            points=points
        )
        db.add(user_warn)
        db.commit()
    except IntegrityError:
        db.rollback()
    except Exception as e:
        db.rollback()

async def update_warn(id_user, points):
    try:
        user_warn = await get_by_user_id(id_user)
        user_warn.points = points
        db.commit()
    except IntegrityError:
        db.rollback()
    except Exception as e:
        db.rollback()

async def warn_without_points(id_user) -> bool:
    user_warn = await get_by_user_id(id_user)
    print(user_warn)
    print(user_warn.points)
    return True if user_warn.points <= 0 else False