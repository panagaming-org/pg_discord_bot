from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import model.dao.banned_domain_dao as banned_domain_dao
import settings.settings as settings
import api.client_api as client_api

DATABASE_URL = "sqlite:///instance/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
db = SessionLocal()

def initialice_db():
    base.metadata.create_all(bind=engine)

def reaload_database():
    domains = client_api.get_domains()
    for domain in domains:
        banned_domain_dao.add_from_json(domain)