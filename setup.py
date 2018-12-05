import check_status
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import logging

cred = credentials.Certificate('your-json-file-here.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-url-here.firebaseio.com/'
})


ref = db.reference('Locations')                                                  # getting all the locations from our database 
locations = ref.get()

def updateDict():
    for key, val in locations.items():                                           # iterates over each location in locations
        try:
            response_in_milliseconds = round(check_status.ping_server(val[0]))      # grabs the response from ping
            main_status = check_status.check_ms(key, response_in_milliseconds)       # uses response to get our status code
            str_response_in_milliseconds = str(response_in_milliseconds)

            ref = db.reference('/')
            locations_ref = ref.child('Locations')
            locations_ref.update({ key : [ val[0], main_status, str_response_in_milliseconds + 'ms' ]})

        except TypeError:
            logging.basicConfig(filename='setup.log', 
                                format='%(asctime)s %(message)s', 
                                datefmt='%m/%d/%Y %I:%M:%S %p', 
                                level=logging.DEBUG)
            logging.info('A TyperError has occured')
            logging.info("Type NoneType doesn't define __round__ method ERROR Has occured.")

def run():
    updateDict()

if __name__ == '__main__':
    run()
