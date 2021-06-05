from handlers.RoomHandler import CreateRoomHandler
from handlers.EnterRoomHandler import EnterRoomHandler
from handlers.PlayersHandler import PlayersHandler
from handlers.DropCardHandler import DropCardHandler

def add_routes(api):
    api.add_resource(CreateRoomHandler, '/createRoom')
    api.add_resource(EnterRoomHandler, '/enterRoom')
    api.add_resource(PlayersHandler, '/getPlayers')
    api.add_resource(DropCardHandler, '/dropCard')


