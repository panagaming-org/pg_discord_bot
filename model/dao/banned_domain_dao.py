from opcode import hasexc
from sqlite3 import IntegrityError

import sqlalchemy

from instance.database import db
from model.entity.BannedDomain import BannedDomain

def get_all():
    domains = db.query(BannedDomain).all()
    return domains

async def get_by_domain(domain):
    try:
        dom = db.query(BannedDomain).filter(BannedDomain.domain == domain).first()
        return dom
    except sqlalchemy.exc.PendingRollbackError:
        db.rollback()
        return db.query(BannedDomain).filter(BannedDomain.domain == domain).first()
    
def add_from_json(domain_json):
    try:
        domain = BannedDomain(
            domain = domain_json['domain'],
            category = domain_json['category']
        )
        db.add(domain)
        db.commit()
    except IntegrityError:
        db.rollback() 
    except Exception as e:
        db.rollback()
