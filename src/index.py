from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send, disconnect, emit, join_room
from flask_login import current_user
from random import randint
from logic.logic import Match
import json
import copy
import time
import asyncio

from flask_restful import Api
from api import routes
from pusher import pusher
from components.Lobby import Lobby

# import psycopg2

app = Flask(__name__)
api = Api(app=app)
routes.add_routes(api=api)

lobby = Lobby()
print(lobby)
app.config['SECRET_KEY'] = 'mysecret'

roomsCreated = []
activeRooms = {} #contains room ids and their corresponding connected users
player_card = {}
lobby = {}

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
pusher.add_pusher(socketIo)

def updateCardCountToRoom(room, id):
    playersList = activeRooms.get(room)
    for index, playerid in enumerate(playersList):
        if(playerid != id): # send communication only to other players
            game_obj = copy.deepcopy(lobby.get(int(room)))
            playerCard = game_obj.get('player_card')
            for key in playerCard: # keep ony self data
                if (key != playerid):
                    emptyCards = {
                        'cards': None   
                    }
                    playerCard.get(key).update(emptyCards)
            socketIo.emit('drop_card', {'data': game_obj}, room=playerid)


@app.route('/dropCard', methods=['POST'])
def dropCard():
    room = json.loads(request.data.decode('utf-8')).get('room')
    card = json.loads(request.data.decode('utf-8')).get('card')
    id = json.loads(request.data.decode('utf-8')).get('id')
    game_local = json.loads(request.data.decode('utf-8')).get('game')
    game_global = lobby.get(int(room))
    playerCount = len(activeRooms.get(room))
    round_one = game_global.get('current_round')
    existing = len(round_one)
    condition = conditionForOneRound(room, id, card)
    if condition is not False:
        print("correct case")
        round_one[existing+1] = {
            'id': id,
            'card': card,
        }
        # on card drop, update both local and global game object and return upated local game object to the player
        # for other players emit the updated player object's totalCount, not for the current player
        player_card_local = game_local.get('player_card').get(id)
        player_card_global = game_global.get('player_card').get(id)
        
        player_card_local.get('cards').remove(card) # remove from list
        player_card_local['totalCards'] =  player_card_local.get('totalCards') - 1
        
        player_card_global.get('cards').remove(card) # remove from list
        player_card_global['totalCards'] =  player_card_global.get('totalCards') - 1
        
        if condition == 'winning_flow':
            # check for highest
            # update center_cards, current_round and push all the cards to highest id
            init_draw = round_one.get(1).get('card').split("_")[1]
            loserId = checkForHighestDraw(game_local.get('current_round'), init_draw)
            game_global = pushCardToLoser(room, loserId, round_one)
            
            game_global['current_round'] = {}
            game_local['current_round'] = {}
        else:
            if (existing+1) == playerCount:
                # exit round - reinitialize round_one and move the object to center_cards
                game_local['center_cards'].append(round_one)
                game_local['current_round'] = {}

                game_global['center_cards'].append(round_one)
                game_global['current_round'] = {}
            else:
                game_local['current_round'] = round_one
                game_global['current_round'] = round_one    
        updateCardCountToRoom(room, id)
        return jsonify({'data': game_local})
    else:
        print("wrong case")
        return jsonify({'data': game_local})
    

app.debug = True
app.host = 'localhost'

def getPrecedence(card):
    order = {
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    if str(card) in order:
        return order.get(card)
    else:
        return card

def pushCardToLoser(room, loserId, round_one):
    game_global = lobby.get(int(room))
    current_loser_cards = game_global.get('player_card').get(loserId).get('cards')
    for key in round_one:
        card = round_one[key].get('card') 
        current_loser_cards.append(card)
        game_global.get('player_card').get(loserId)['totalCards'] = len(current_loser_cards)
    print("after loser data update--->")
    print(game_global)
    return game_global


def checkForHighestDraw(cardList, init_draw):
    maxCard = 2 # init with min value
    for i in cardList:
        print("Failedd->>")
        print(cardList.get(i))
        card = cardList.get(i).get('card').split("_")[0]
        cardNumber = getPrecedence(card)
        # card value goes from J to Q, K till A. A takes highst precedence
        if int(maxCard) <= int(cardNumber):
            maxCard = cardNumber
            maxId = cardList.get(i).get('id')
    return maxId

def conditionForOneRound(room, id, card):
    # check the length of the current_round array
    # compare the list of cards for every drop
    # same symbol np, different symbol, check if valid drop
    # if not return card
    # if valid compare the largest and send everything to that person
    # update game obj
    # one successfl round,clear the current_round array and dump in center cards

    # check if current card drawn is valid before updating current_round object in game object
    # return for initial draw - no validation

    falsyMove = False
    differentSymbolDrawn = False
    game = lobby.get(int(room))
    cardList = game.get('current_round')
    if len(cardList) == 0:
        print("game returned")
        return True
    print(game)
    init_draw = cardList.get(1).get('card').split("_")[1]
    symbol = card.split("_")[1]
    if symbol != init_draw:
        print('case 1')
        print(card)
        differentSymbolDrawn = True
        # get the player's cards
        currentCardList = game.get('player_card').get(id).get('cards')
        for i in range(0,len(currentCardList),1):
            symbolAvailable = currentCardList[i].split("_")[1]
            if symbolAvailable == init_draw:
                falsyMove = True
                return
        # check if valid drop
        # loop through game.player_card[cardList.get(i).id]
    if falsyMove == True:
        print("wrongggg--->>>")
        print(card)
        print(init_draw)
        # user should redraw correct card - user selected different smbol though he have the correct one
        return False
    elif differentSymbolDrawn == True and falsyMove == False:
        # user don't have the correct symbol, a valid draw
        # update game object here
        # then check for highest
        # quit the round and send all to the one who drew highest card
        print("winning case")
        return 'winning_flow'
        # checkForHighestDraw(cardList, init_draw)
    else:
        print("happy flow")
        return 'happy_flow'
        # happy flow - stash set


def setPlayersTurn(room):
    clientArr = activeRooms.get(room)
    print("------------------------------")
    print("proper order-->")
    print(clientArr)
    print("------------------------------")
    i = 0
    while True:
        socketIo.emit("player_turn", clientArr[i], to=room)
        time.sleep(7)   
        i += 1
        if i == len(clientArr):
            i = 0

def checkForPlayers(room):
    cardsDistributed = 0
    clientArr = activeRooms.get(room)
    if len(clientArr) == 4:
        asd = Match()
        cards = asd.distributeCards()
        for index, client in enumerate(clientArr):
            player_card[client] = {
                'room': room,
                'cards': cards[index],
                'totalCards': 13
            }
        # create a room in lobby which is a game object
        lobby[room] = {
            'player_card': player_card,
            'center_cards': [],
            'current_round': {},
            'active_player': ''
        } 
        game = lobby.get(room)
        response = copy.deepcopy(game)
        for index, client in enumerate(clientArr):
            playerCard = copy.deepcopy(game.get('player_card'))
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
        if cardsDistributed == 4:
            setPlayersTurn(room)


# @socketIo.on('connect')
# def test_connect():
#     print("------------------------------")
#     print('[INFO] Web client connected: {}'.format(request.sid))
#     print("------------------------------")
#     send(request.sid)

@socketIo.on('disconnect')  
def test_connect():
    print("------------------------------")
    print('[INFO] Web client disconnected: {}'.format(request.sid))
    print("------------------------------")

# @socketIo.on('join')
# def handle_join_room_event(data):
#     username = data['sessionId']
#     room = data['room']
#     join_room(room)
#     # send(username, to=room)
#     socketIo.emit('join_room_announcement', activeRooms.get(room), to=room)
#     checkForPlayers(room)

@socketIo.on("message")
def handleMessage(msg):
    send(msg)
    return None


if __name__ == '__main__':
    socketIo.run(app)