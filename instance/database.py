from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import model.dao.banned_domain_dao as banned_domain_dao
import settings.settings as settings
from api.client_api import ClientAPI

DATABASE_URL = "sqlite:///instance/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
db = SessionLocal()

def initialice_db():
    base.metadata.create_all(bind=engine)

def reaload_database():
    api_url = settings.get_api_backend()
    client = ClientAPI(api_url)

    domains = client.get_domains()
    for domain in domains:
        banned_domain_dao.add_from_json(domain)