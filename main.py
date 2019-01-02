from flask import Flask, request, render_template, redirect
import setup
import updateDB
import json
import time
import timer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import logging

app = Flask(__name__)

@app.route('/')
def index():
    # getting all the locations from our database 
    ref = db.reference('Locations')
    LOCATIONS_DICTS = ref.get()
    return render_template('index.html', locations_dicts=LOCATIONS_DICTS)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        location_name = request.form['location_name']
        ipAddress = request.form['ipAddress']
        '''if location_name or ipAddress == '':
            pass
            print(location_name)
            print(ipAddress)
            print("Passed.")
        else:
            updateDB.add(location_name, ipAddress)
            print("Database updated.")
            redirect('/')'''
        
        updateDB.add(location_name, ipAddress)

    return render_template('add-location.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    # getting all the locations from our database 
    ref = db.reference('Locations')
    LOCATIONS_DICTS = ref.get()

    if request.method == 'POST':
        location_name = request.form['location_name']
        #print(location_name)
        updateDB.remove(location_name)

    return render_template('remove-location.html', locations=LOCATIONS_DICTS)

@app.route('/success')
def success():
    return render_template('success.html')
    
app.run(debug=True, host='0.0.0.0')
