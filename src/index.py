from flask import Flask, jsonify, request;
from flask_socketio import SocketIO, send, disconnect, emit
from flask_login import current_user
from random import randint
from logic import Match
import json
# import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

roomsCreated = []
activeRooms = {} #contains room ids and their corresponding connected users

@app.route('/createRoom')
def createRoom():
    room = randint(1000, 9999)
    roomsCreated.append(room)
    # activeRooms[room] = [ request.sid ]
    
    return jsonify({'room': room})

@app.route('/enterRoom', methods=['POST'])
def joinGame():
    data = json.loads(request.data.decode('utf-8')).get('data') 
    result = None
    if int(data) in roomsCreated:
        print('condition true')
        result = data
    return jsonify({'room': result})

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

@socketIo.on("message")
def handleMessage(msg):
    send(msg, broadcast=True)
    return None


if __name__ == '__main__':
    socketIo.run(app)