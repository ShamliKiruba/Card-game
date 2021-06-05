from .Game import Game
class Room():
    def __init__(self):
        print("Room Class")
        self._player_count = 0
        self._players = []
        self._is_game_started = False
        self._game = {} # refer Game class - init once game starts
    
    def setPlayers(self, player_id):
        self._players.append(player_id)
        self.updatePlayerCount()
    
    def updatePlayerCount(self):
        self._player_count = len(self._players)

    def getPlayers(self):
        return self._players

    def setGameStatus(self, status):
        self._is_game_started = status
    
    def getGameStatus(self, status):
        return self._is_game_started
    
    def setGame(self, val: Game):
        self._game = val