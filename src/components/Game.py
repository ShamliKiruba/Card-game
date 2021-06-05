class Game:
    def __init__(self):
        print("init Game function")
        self._player_card = {}
        self._current_round = {}
        self._center_cards = []
        self._current_round_count = 0
    
    def addPlayerCards(self, id, cardData):
        self._player_card[id] = cardData
    
    def setAllPlayerCards(self, cardData):
        self._player_card = cardData
    
    def getPlayerCards(self, id):
        return self._player_card.get(id)

    def getAllPlayerCards(self, id):
        return self._player_card
    
    def setCurrentRound(self, obj):
        self._current_round[self._current_round_count+1] = obj
    
    def getCurrentRound(self):
        return self._current_round
    
    def setCenterCards(self, obj):
        self._center_cards.append(obj)
    
    def getCenterCardsCount(self):
        return len(self._center_cards)
