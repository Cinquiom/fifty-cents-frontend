class Card:

    RANKS = '3 4 5 6 7 8 9 10 J Q K A 2 JOKER'.split()

    def __init__(self, rank):
        self.rank = rank

    def __repr__(self):
        return self.rank

    @property
    def value(self):
        i = self.RANKS.index(self.rank)
        if i == 13: return 50
        if i > 10: return 20
        if i > 4: return 10
        return 5
        
    @property
    def count(self):
        return 2 if self.RANKS.index(self.rank) == 13 else 4
        
    @property
    def is_wildcard(self):
        return self.RANKS.index(self.rank) > 11
        
        
if __name__ == "__main__":
    
    cards = [Card(r) for r in Card.RANKS]
    
    for c in cards:
        print(c.rank, c.value, c.count, c.is_wildcard) 
        