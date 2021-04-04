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


def satellite(id):
    print("Sat data was requested")
    response = requests.get('https://api.n2yo.com/rest/v1/satellite/positions/' +
                            str(id) + '/0/0/0/2/&apiKey=ZVZQAW-QN6CAQ-FUR8SR-4O4V')

    # make a record in firebase

    [response.json()['info']['satname'], response.json()['positions'][0]
     ['satlatitude'], response.json()['positions'][0]['satlongitude']]


while True:
    satellite(25544)
    time.sleep(60)


while True:
    satellite(20580)
    time.sleep(60)


@app.route('/satdata/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def iss(id):
    print("Sat data was requested")
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    # dummy for now
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
