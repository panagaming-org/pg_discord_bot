from sqlalchemy import Column, Integer, String
from instance.database import base

class UserWarn(base):
    __tablename__ = "user_warn"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, unique=True)
    points = Column(Integer, nullable=False)

    def __init__(self, id_user, points):
        self.id_user = id_user
        self.points = points