from .Room import Room

class Lobby():
    def __init__(self):
        print("init Lobby Class")
        self._lobby = {}
    
    def setRoom(self, room_id, value: Room):
        # create an instance of Room Class and assign it here
        self._lobby[room_id] = value
        print("setRoom--->")
        print(self._lobby)

    def getRoomList(self):
        return self._lobby.keys()

    def getRoomData(self, room_id):
        print("getRoomData--->")
        print(self._lobby)
        return self._lobby.get(room_id)
