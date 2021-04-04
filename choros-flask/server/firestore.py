import os
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


parser = reqparse.RequestParser()
parser.add_argument('longitude', action='append')
parser.add_argument('latitude', action='append')
parser.add_argument('satId')
parser.add_argument('satName')


def getSatellite(satID):
    response = requests.get('https://api.n2yo.com/rest/v1/satellite/positions/' +
                            str(satID) + '/0/0/0/2/&apiKey=ZVZQAW-QN6CAQ-FUR8SR-4O4V')
    print(response.json())
    satellite = {'satName': response.json()['info']['satname'], 'id': response.json()['info']['satid'], 'longitude': response.json()['positions'][0]
                 ['satlongitude'], 'latitude': response.json()['positions'][0]['satlatitude']}

    return satellite


class Satellite(object):
    def __init__(self, satName, satId, latitude=[], longitude=[]):
        self.satName = satName
        self.satId = satId
        self.latitude = latitude
        self.longitude = longitude

    def to_sat(self):
        satellite = {
            'satId': self.satId,
            'satName': self.satName,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
        return satellite

    def __repr__(self):
        return 'Satellite(name={}, Satellite ID = {}, Satilite Longitude = {} , Satellite Latitdue = {})'.format(self.satName, self.satId, self.latitude, self.longitude)


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


# class SatelliteLongLat(Resource):
#     def get(self):
#         doc_ref = db.collection('satellites').document(
#             '25544').collection('latlong')
#         docs = doc_ref.stream()
#         longLatList = {}
#         for doc in docs:
#             longLatList[doc.id] = doc.to_dict()
#         return longLatList


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
        currentSatData = getSatellite(satId)
        print(currentSatData)
        doc_ref = db.collection('satellites').document(satId)
        # print(satId)
        if doc_ref:
            print(doc_ref.get())
            return doc_ref.get().to_dict()

        return None

    def delete(self, taskid):
        sat_ref = db.collection('satellites')
        sat_ref.document(taskid).delete()
        return True, 201


api.add_resource(SatelliteList, '/satellites')
api.add_resource(SatelliteListById, '/satellites/<satId>')


if __name__ == '__main__':
    firestoreApp.run(debug=True)
