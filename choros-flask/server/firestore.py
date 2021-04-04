import os
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort, reqparse
from firebase_admin import credentials, firestore, initialize_app
import time
import requests
from google.cloud import firestore
import firebase


db = firestore.Client()
firestoreApp = Flask(__name__)
api = Api(firestoreApp)

cors = CORS(firestoreApp, resources={r"/foo": {"origins": "*"}})
firestoreApp.config['CORS_HEADERS'] = 'Content-Type'
firestoreApp.config.from_object(__name__)

# enable CORS
CORS(firestoreApp, resources={r'/*': {'origins': '*'}})


parser = reqparse.RequestParser()
parser.add_argument('longitude', action='append')
parser.add_argument('latitude', action='append')
parser.add_argument('satId')
parser.add_argument('satName')
parser.add_argument('satDescription')
parser.add_argument('pictureUrl')
parser.add_argument('launchDate')


def getSatellite(satID):
    response = requests.get('https://api.n2yo.com/rest/v1/satellite/positions/' +
                            str(satID) + '/0/0/0/2/&apiKey=ZVZQAW-QN6CAQ-FUR8SR-4O4V')
    print(response.json())
    satellite = {'satName': response.json()['info']['satname'], 'id': response.json()['info']['satid'], 'longitude': response.json()['positions'][0]
                 ['satlongitude'], 'latitude': response.json()['positions'][0]['satlatitude']}

    return satellite


class Satellite(object):
    def __init__(self, satName, satId, description, pictureUrl, launchDate, latitude=[], longitude=[], ):
        self.satName = satName
        self.satId = satId
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.pictureUrl = pictureUrl
        self.launchDate = launchDate

    def to_sat(self):
        satellite = {
            'satId': self.satId,
            'satName': self.satName,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description,
            'pictureUrl': self.pictureUrl,
            'launchDate': self.launchDate
        }
        return satellite

    def __repr__(self):
        return 'Satellite(name={}, Satellite ID = {}, Satilite Longitude = {} , Satellite Latitdue = {}, Satellite Description = {} , Satellite Picture = {})'.format(self.satName, self.satId, self.latitude, self.longitude, self.description)


class SatelliteList(Resource):
    def get(self):
        sat_ref = db.collection(u'satellites')
        docs = sat_ref.stream()
        satellites = {}
        for doc in docs:
            satellites[doc.id] = doc.to_dict()
        return satellites

    def post(self):
        args = parser.parse_args()
        print(args)
        satellite = Satellite(satName=args[u'satName'], satId=args[u'satId'], longitude=args[
                              u'longitude'], latitude=args[u'latitude'])
        satId = satellite.satId
        db.collection(u'satellites').document(satId).set(satellite.to_sat())
        return satellite.to_sat(), 201


class SatelliteListById(Resource):
    def put(self, satId):
        args = parser.parse_args()
        currentSatData = getSatellite(satId)
        print(args)
        sat_ref = db.collection('satellites').document(satId)
        longitude = currentSatData.get('longitude')
        latitude = currentSatData.get('latitude')
        print(longitude)
        sat_ref.update(
            {u'longitude': firestore.ArrayUnion([str(longitude)]), u'latitude': firestore.ArrayUnion([str(latitude)])})
        return sat_ref.get().to_dict(), 201

    def get(self, satId):
        args = parser.parse_args()
        currentSatData = getSatellite(satId)
        print(args)
        sat_ref = db.collection('satellites').document(satId)
        longitude = currentSatData.get('longitude')
        latitude = currentSatData.get('latitude')
        print(longitude)
        sat_ref.update(
            {u'longitude': firestore.ArrayUnion([str(longitude)]), u'latitude': firestore.ArrayUnion([str(latitude)])})
        return sat_ref.get().to_dict(), 201

    def delete(self, taskid):
        sat_ref = db.collection('satellites')
        sat_ref.document(taskid).delete()
        return True, 201


api.add_resource(SatelliteList, '/satellites')
api.add_resource(SatelliteListById, '/satellites/<satId>')


if __name__ == '__main__':
    firestoreApp.run(debug=True)
