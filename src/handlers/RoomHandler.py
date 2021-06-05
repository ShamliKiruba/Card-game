from flask_restful import Resource, Api
from flask import Flask, jsonify, request
import json
from components.Lobby import Lobby
from components.Room import Room
from random import randint
# from pusher.pusher import send_pusher_events
from common.constants import EventList

class CreateRoomHandler(Resource):
    def __init__(self):
        print("init function of CreateRoomHandler")
    
    def post(self):
        session_id = json.loads(request.data.decode('utf-8')).get('sessionId') 
        
        lobby = Lobby()
        room_id = randint(1000, 9999)
        while room_id in lobby.getRoomList():
            room_id = randint(1000, 9999)
        room = Room()
        room.setPlayers(session_id)

        lobby.setRoom(room_id, room)
        return jsonify({'room': room_id})

        # sessionId = json.loads(request.data.decode('utf-8')).get('sessionId') 
        # print("sessionId--->")
        # return jsonify({'sessionId': sessionId})

class JoinRoomHandler():
    def __init__(self):
        print("init function of JoinRoomHandler")
    
    def checkForPlayers(self, room_id):
        print("checkForPlayers function of JoinRoomHandler")
        
        lobby = Lobby()
        asd = lobby.getRoomData(room_id)
        print(asd)
        # send_pusher_events(EventList.JOIN_ROOM_ANNOUNCEMENT, room.getPlayers())