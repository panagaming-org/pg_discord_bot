from sqlalchemy import Column, Integer, String

from instance.database import base

class BannedDomain(base):
    __tablename__ = "banned_domain"
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(1000), unique=True, nullable=False, index=True)
    category = Column(String(500))

    def __init__(self, domain, category):
        self.domain = domain
        self.category = category