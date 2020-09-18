import random
from app.fiftycents.entities.card import Card

class Deck():
    def __init__(self, size=1, empty = False):
        self.cards = []
        
        if not empty:
            self.cards = [Card(r) for r in Card.RANKS
                                  for i in range(Card(r).count) 
                                  for j in range(size)]
            self._shuffle()
                                             
    def __repr__(self):
        return '<Deck {}>'.format(len(self.cards))

    def _shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop()
    
    def bury(self, card):
        self.cards.insert(0, card)
        
    def cover(self, card):
        self.cards.append(card)
    
if __name__ == "__main__":
    
    d = Deck()
    d._reset(3)
    
    from collections import Counter
    
    counter = Counter([c.rank for c in d.cards])
    print(counter)