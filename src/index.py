from flask import Flask, jsonify, request;
from flask_socketio import SocketIO, send, disconnect, emit, join_room
from flask_login import current_user
from random import randint
from logic import Match
import json
# import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

roomsCreated = []
activeRooms = {} #contains room ids and their corresponding connected users

@app.route('/createRoom', methods=['POST'])
def createRoom():
    sessionId = json.loads(request.data.decode('utf-8')).get('sessionId') 
    room = randint(1000, 9999)
    roomsCreated.append(room)
    activeRooms[room] = [ sessionId ]
    print("activeRooms--->")
    print(activeRooms)
    return jsonify({'room': room})

@app.route('/enterRoom', methods=['POST'])
def joinGame():
    sessionId = json.loads(request.data.decode('utf-8')).get('sessionId') 
    data = int(json.loads(request.data.decode('utf-8')).get('data'))
    result = None
    if data in roomsCreated:
        activeRooms[data].append(sessionId)
        result = data
        
    return jsonify({'room': result})

@app.route('/getPlayers', methods=['POST'])
def getPlayers():
    room = json.loads(request.data.decode('utf-8')).get('room')
    players = activeRooms.get(room)
    return jsonify({'players': players})

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

@socketIo.on('connect')
def test_connect():
    print("------------------------------")
    print('[INFO] Web client connected: {}'.format(request.sid))
    print("------------------------------")
    send(request.sid)

@socketIo.on('disconnect')  
def test_connect():
    print("------------------------------")
    print('[INFO] Web client disconnected: {}'.format(request.sid))
    print("------------------------------")

@socketIo.on('join')
def handle_join_room_event(data):
    username = data['sessionId']
    room = data['room']
    join_room(room)
    # send(username, to=room)
    socketIo.emit('join_room_announcement', activeRooms.get(room), to=room)

@socketIo.on("message")
def handleMessage(msg):
    send(msg)
    return None


if __name__ == '__main__':
    socketIo.run(app)