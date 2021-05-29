from flask import Flask, jsonify, request;
from flask_socketio import SocketIO, send, disconnect, emit, join_room
from flask_login import current_user
from random import randint
from logic import Match
import json
import copy
import time
import asyncio
# import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

roomsCreated = []
activeRooms = {} #contains room ids and their corresponding connected users
player_card = {}
game = {}

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

@app.route('/dropCard', methods=['POST'])
def dropCard():
    room = json.loads(request.data.decode('utf-8')).get('room')
    card = json.loads(request.data.decode('utf-8')).get('card')
    id = json.loads(request.data.decode('utf-8')).get('id')
    round_one = game.get(int(room)).get('current_round')
    player_card = game.get(int(room)).get('player_card').get(id)
    player_card.get('cards').remove(card) # remove from list
    player_card['totalCards'] =  player_card.get('totalCards') - 1
    existing = len(round_one)
    round_one[existing+1] = {
        id: card,
    }
    response = game.get(int(room))
    # conditionForOneRound(room)
    socketIo.emit('drop_card', {'data': response}, to=room)
    return jsonify({'data': response})

app.debug = True
app.host = 'localhost'

def checkForHighestDraw(cardList, init_draw):
    maxCard = 2
    for i in range(0,len(cardList),1):
        cardNumber = cardList.get(i).get('card')[0:1]
        if maxCard <= cardNumber:
            maxCard = cardNumber
            maxId = cardList.get(i).get('id')

def conditionForOneRound(room):
    # check the length of the current_round array
    # compare the list of cards for every drop
    # same symbol np, different symbol, check if valid drop
    # if not return card
    # if valid compare the largest and send everything to that person
    # update game obj
    # one successfl round,clear the current_round array and dump in center cards
    falsyMove = False
    differentSymbolDrawn = False
    game_room = game.get(int(room))
    cardList = game_room.get('current_round')
    init_draw = cardList.get('1').get('card')[2:]
    for i in range(0,len(cardList),1):
        symbol = cardList.get(i).get('card')[2:]
        if symbol != init_draw:
            differentSymbolDrawn = True
            # get the player's cards
            currentCardList = game_room.player_card.get(cardList.get(i).get('id'))
            for index, check in currentCardList:
                symbolAvailable = currentCardList[i][0][2:]
                if symbolAvailable == init_draw:
                    falsyMove = True
                    return
            # check if valid drop
            # loop through game_room.player_card[cardList.get(i).id]
    if falsyMove == True:
        # redraw correct card
        return None
    elif differentSymbolDrawn == True:
        checkForHighestDraw(cardList, init_draw)
    else:
        print("else")
        # continue round
        # if over, happy flow - stash set

    playerCount = len(activeRooms.get(room))


def setPlayersTurn(room):
    clientArr = activeRooms.get(room)
    print("------------------------------")
    print("proper order-->")
    print(clientArr)
    print("------------------------------")
    i = 0
    while True:
        socketIo.emit("player_turn", clientArr[i], to=room)
        time.sleep(10)   
        i += 1
        if i == len(clientArr):
            i = 0


def checkForPlayers(room):
    cardsDistributed = 0
    clientArr = activeRooms.get(room)
    if len(clientArr) == 2:
        asd = Match()
        cards = asd.distributeCards()
        for index, client in enumerate(clientArr):
            player_card[client] = {
                'room': room,
                'cards': cards[index],
                'totalCards': 13
            }
        game[room] = {
            'player_card': player_card,
            'center_cards': {},
            'current_round': {},
            'active_player': ''
        } 
        response = copy.deepcopy(game.get(room))
        for index, client in enumerate(clientArr):
            playerCard = copy.deepcopy(game.get(room).get('player_card'))
            for key in playerCard:
                if key != client:
                    emptyCards = {
                        'cards': None
                    }
                    playerCard.get(key).update(emptyCards)
                else:
                    pass
                response.get('player_card').update(playerCard)
            socketIo.emit('distribute_cards', response, room=client)
            cardsDistributed += 1
        if cardsDistributed == 2:
            setPlayersTurn(room)


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
    checkForPlayers(room)

@socketIo.on("message")
def handleMessage(msg):
    send(msg)
    return None


if __name__ == '__main__':
    socketIo.run(app)