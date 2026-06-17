from instance.database import db
from model.entity.BannedDomain import BannedDomain

def get_all():
    domains = db.query(BannedDomain).all()
    return domains

def get_by_domain(domain):
    dom = db.query(BannedDomain).filter(BannedDomain.domain == domain).first()
    return dom

def add_from_json(domain_json):
    domain = BannedDomain(
        domain = domain_json['domain'],
        category = domain_json['caegory']
    )
    db.add(domain)
    db.commit()