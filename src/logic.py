import numpy as np
import random

class Match:
    def __init__(self):
        self._deck = 52
        self._categories = ['club', 'spade', 'heart', 'diamond']
        self._cards = [1,2,3,4,5,6,7,8,9,10,'J','Q','K']
        self._club = ['A_club','2_club','3_club','4_club','5_club','6_club','7_club','8_club','9_club','10_club','J_club','Q_club','K_club']
        self._spade =  ['A_spade','2_spade','3_spade','4_spade','5_spade','6_spade','7_spade','8_spade','9_spade','10_spade','J_spade','Q_spade','K_spade']
        self._heart =  ['A_heart','2_heart','3_heart','4_heart','5_heart','6_heart','7_heart','8_heart','9_heart','10_heart','J_heart','Q_heart','K_heart']
        self._diamond = ['A_diamond','2_diamond','3_diamond','4_diamond','5_diamond','6_diamond','7_diamond','8_diamond','9_diamond','10_diamond','J_diamond','Q_diamond','K_diamond']
        self._group = []
        
    def divideCards(self, members):
        return (52/members)
    
    def distributeCards(self):
        for i in range(0, 13):
            self._group.append(self._club[i])
            self._group.append(self._spade[i])
            self._group.append(self._heart[i])
            self._group.append(self._diamond[i])

        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)                 
        random.shuffle(self._group)
        cards_all = self._group 

        final_all = []
        for n in range(4):
            final = []
            for num in range(13):
                element = random.choice(cards_all)
                final.append(element)
                cards_all = [num for num in cards_all if num != element]
            final_all.append(final)
        
        # print(final_all)
        return final_all


asd = Match()
asd.distributeCards()