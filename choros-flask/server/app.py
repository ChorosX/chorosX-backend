from flask_cors import CORS, cross_origin
from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify
import json
import requests
import time

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

satellites = [20580,
                25544,
                25994,
                26871,
                27386,
                28790,
                29155,
                31135,
                33591,
                37849,
                39444,
                40967,
                41759,
                42738,
                42740,
                ]

while True:
    for satID in satellites:
        requests.get('http://127.0.0.1:5000/satellites/' + str(satID))
        print(str(satID) + ' updated')
    time.sleep(15)

if __name__ == '__main__':
    app.run(debug=True)
