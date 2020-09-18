import math
from collections import Counter
from itertools import dropwhile

class NoCoinsRemainingError(Exception): pass
class CardNotInHandError(Exception): pass

class Player():
    
    def __init__(self):
        self.hand = []
        self.played_cards = []
        self.down = False
        self.coins = 10
        self.total_score = 0
        
    def add_card(self, card):
        self.hand.append(card)
        
    def get_current_score(self):
        up = sum([c.value for c in self.played_cards])
        down = sum([c.value for c in self.hand])
        
        return up - down
    
    # Messy function to determine if a hand is valid.
    # Steps:
    #    1) Get all normal cards
    #    2) Get all wildcards
    #    3) 
    def get_playable_sets(self, hand, n, s):
        counter = Counter([c.rank for c in hand])
        wildcards = counter.pop('2', 0) + counter.pop('JOKER', 0)
        for k, v in dropwhile(lambda x: x[1] >= math.ceil(s/2.0), counter.most_common()):
            del counter[k]
               
        playable_sets = {}
        playable_sets_num = 0
        for k in counter:
            
            # Special exception: splitting extra-large pairs into two sets
            if n > 1 and counter[k] >= s and wildcards >= n*s - counter[k]:
                playable_sets[k] = (counter[k], n*s - counter[k])
                wildcards = wildcards - n*s + counter[k]
                playable_sets_num += 1
            else:
                wildcards_needed = s - counter[k]
                if wildcards_needed <= wildcards:
                    playable_sets[k] = (counter[k], max(wildcards_needed, 0))
                    wildcards = wildcards - max(wildcards_needed, 0)
            
        playable_sets_num += len(playable_sets)
        return playable_sets if playable_sets_num >= n else None 

    def check_playable_sets(self, hand, set_size, set_num):
        return self.get_playable_sets(hand, set_size, set_num) != None
    
    def spend_coin(self):
        if self.coins <= 0:
            raise NoCoinsRemainingError
        self.coins = self.coins - 1
        
    def toss(self, card):
        for c in self.hand:
            if card == c.rank:
                self.hand.remove(c)
                return c
        raise CardNotInHandError
        