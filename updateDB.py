import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import setup


def add(new_location, ipaddress):

    ref = db.reference('/')
    locations_ref = ref.child('Locations')
    locations_ref.update({ new_location : [ ipaddress, "green", "9ms" ]})  

def remove(location):

    ref = db.reference('/Locations')
    locations_ref = ref.child(location)
    locations_ref.set({})
