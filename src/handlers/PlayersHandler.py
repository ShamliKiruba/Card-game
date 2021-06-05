from flask_restful import Resource, Api
from flask import Flask, jsonify, request
import json

class PlayersHandler(Resource):
    def __init__(self):
        print("init function of PlayersHandler")
    
    def post(self):
        sessionId = json.loads(request.data.decode('utf-8')).get('sessionId') 
        print("sessionId--->")
        return jsonify({'sessionId': 'sessionId created'})
