from flask import request
from flask_socketio import SocketIO, send, disconnect, emit, join_room
from handlers.RoomHandler import JoinRoomHandler

def add_pusher(socketIo):
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
        join_room_obj = JoinRoomHandler()
        join_room_obj.checkForPlayers(room)

    @socketIo.on("message")
    def handleMessage(msg):
        send(msg)
        return None


def send_pusher_events(socketIo, event_name, data, is_broadCast, id):
    '''
        If it is a broadcast mesage, then the third param is 
        (to=room_id) or  (room=client_id) 
    '''
    if is_broadCast is True:
        socketIo.emit(event_name, data, to=id)
    else:
        socketIo.emit(event_name, data, room=id)