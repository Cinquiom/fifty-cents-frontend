from __future__ import division

from collections import Counter
from itertools import chain, combinations, islice
from copy import deepcopy

from app.fiftycents.entities.player import Player
from app.fiftycents.entities.deck import Deck
from app.fiftycents.entities.card import Card

class FiftyCentsAI(Player):
    def __init__(self, difficulty):
        Player.__init__(self)
        self.difficulty = difficulty
        self.player_bought = set()
    
    """
        Given a number of cards to draw (1, 3, 6, 9, etc.) and
        the number of rounds left, find the value of drawing vs buying given
        a mock deck.
    """
    def get_draw_heuristics(self, coins_to_spend, n, s, pile=[]):
        
        hand_copy = [c.rank for c in deepcopy(self.hand)]
        pile_copy = [c.rank for c in deepcopy(pile)]
        
        # First thing we do is remove all cards that we know are not in the deck.
        testingdeck = [c.rank for c in Deck(2).cards]
        for c in chain(hand_copy, pile_copy):
            testingdeck.remove(c)
        
        # Now we get the probability of pulling a specific combination.
        # We use this value to build an "average value" heuristic.
        combos = list(islice(combinations(testingdeck, max(1, 3*coins_to_spend)), self.difficulty))
        num_combos = len(combos)
        down = 0
        
        for x in range(coins_to_spend):
            hand_copy.append(pile_copy.pop())
        
        for c in combos:
            newhand = hand_copy + list(c)
            if self.check_playable_sets([Card(c) for c in newhand], n, s):
                down += 1/num_combos
                
        return down

    def play(self, instructions, cards_in_play):
        
        wild_hand   = list(filter(lambda a: a in ["2", "JOKER"], [c.rank for c in self.hand]))
    
        result = []
        if instructions:
            self.down=True
            for k,v in instructions.items():
                result.append([k for x in range(v[0])] + [wild_hand.pop() for x in range(v[1])])
                
        for play in result:
            for card in play:
                c = self.toss(card)
                self.played_cards.append(c)
        
        if self.down:
            for card in self.hand:
                if card.rank in cards_in_play:
                    c = self.toss(card.rank)
                    self.played_cards.append(c)
                    
        help_lut = {}
        
        print "Hand: {}".format(self.hand)
        print "Played: {}".format(self.played_cards)
        
        # Now we sum the number of cards we have to the help LUT.
        for k,v in dict(Counter([c.rank for c in self.hand])).items():
            if k not in help_lut:
                help_lut[k] = 0
            help_lut[k] += 2 ** v
            
        if "2" in help_lut: help_lut["2"] += 10
        if "JOKER" in help_lut: help_lut["JOKER"] += 15
        
        for c in self.player_bought:
            if c in help_lut:
                help_lut[c] += 10
        
        if help_lut:
            card_to_toss = min(help_lut, key=help_lut.get)
            c = self.toss(card_to_toss)
            print "Threw away {}".format(c)
            return c
        else:
            print "Played our last card."
            return None
    
        