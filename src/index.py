from flask import Flask, jsonify, request;
from flask_socketio import SocketIO, send, disconnect, emit
from flask_login import current_user

from logic import Match
# import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

@socketIo.on('connect')
def test_connect():
    print("------------------------------")
    print('[INFO] Web client connected: {}'.format(request.sid))
    print("------------------------------")
    text = 'Client connected. your id: ' + request.sid
    send(text)

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