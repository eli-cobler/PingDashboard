from typing import List
import os
from sqlalchemy.orm.exc import NoResultFound
import sqlalchemy.sql
from ping_dashboard.data import db_session
from ping_dashboard.data.location import Location

def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'ping_dashboard.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

def get_server_urls() -> List[Location]:
    init_db()

    session = db_session.create_session()
    locations = session.query(Location). \
        all()

    session.close()

    return locations

def sorted_server_urls():
    init_db()

    session = db_session.create_session()
    locations = session.query(Location).\
        order_by(Location.ping.desc()).\
        all()

    session.close()

    return locations

def does_customer_exist(location_id):
    init_db()

    session = db_session.create_session()
    exists = session.query(sqlalchemy.exists().where(Location.id == location_id )).scalar()
    if exists:
        print(f'Customer {location_id} exists.')

    if not exists:
        print(f'Customer {location_id} does not exists.')

    return exists

def remove_customer(location_id):
    init_db()
    session = db_session.create_session()

    location = session.query(Location) \
        .filter(Location.id == location_id) \
        .first()
    session.delete(location)
    session.commit()
    session.close()

def get_anonymize_customers(locations) -> List:

    customer_number = 1
    anonymize_customers = []
    for _ in locations:
        customer_name = f'Cust_{customer_number}'
        anonymize_customers.append(customer_name)
        customer_number += 1

    return anonymize_customers

def update_server(friendly_name, anonymize_name, response_time, ping, location_status, url, status_color, type):
    init_db()

    session = db_session.create_session()

    try:
        s = session.query(Location).filter(Location.id == friendly_name).one()
        # print(f'Location {friendly_name} exists.')

        s.id = friendly_name
        s.anonymized_name = anonymize_name
        s.response_time = response_time
        s.ping = ping
        s.status = location_status
        s.url = url
        s.status_color = status_color
        s.type = type

        session.commit()

    except NoResultFound:
        # print(f'Location {friendly_name} does not exists.')
        s = Location()

        s.id = friendly_name
        s.anonymized_name = anonymize_name
        s.url = url
        s.status = location_status
        s.response_time = response_time
        s.ping = ping
        s.status_color = status_color
        s.type = type

        session = db_session.create_session()
        session.add(s)
        session.commit()