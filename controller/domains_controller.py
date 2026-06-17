import model.dao.banned_domain_dao as banned_domain_dao
from api.client_api import ClientAPI

def insert_many_json(domains):
    for domain in domains:
        try:
            banned_domain_dao.add_from_json(domain)
        except:
            pass