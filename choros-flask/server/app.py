from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import Flask,render_template,url_for,request,redirect, make_response
import json
from flask import Flask, render_template, make_response
import requests

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/satdata/<id>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def heart_rate(id):
    print("Sat data was requested")
    response = requests.get('https://api.n2yo.com/rest/v1/satellite/positions/' + str(id) + '/0/0/0/2/&apiKey=<API KEY>')

    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
