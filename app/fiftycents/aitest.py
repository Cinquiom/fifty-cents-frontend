from __future__ import division

"""
    In this test, we assume the following:
        - No cards have been played
        - 2 decks have been used
        
    When drawing, the AI will generate a heuristics table
    based on a combination with an r of 1.
"""

import random
from fcai import make_deck
from fcai.ai import FiftyCentsAI
from fcai.deck import check_playable

def round_num(n,s):
    return (2*s+n)-6

AI = FiftyCentsAI(10000)
    
for n,s in [(1,3),(2,3),(1,4),(2,4),(1,5),(2,5),(1,6),(2,6)]:
    deck = list(make_deck(2))
    random.shuffle(deck)
    
    AI.reset()
    AI.hand = [deck.pop() for i in range(11)]
    pile = [deck.pop(), deck.pop()]
    
    print "Starting round for {} sets of {}".format(n,s)
    print "{} coins remaining".format(AI.coins)
    print "Spending bias: {}".format(round_num(n, s) - 9)
    while AI.hand:
        draw = AI.get_draw_heuristics(0,n,s,pile=pile)
        buy_one = AI.get_draw_heuristics(1,n,s,pile=pile)
        buy_two = AI.get_draw_heuristics(2,n,s,pile=pile)
        
        print draw, buy_one, buy_two
        
        # Only buy one if we have a really good chance of going down.
        if draw < 0.1 and buy_one > 0.8 and AI.coins > 0 and not AI.down:
            AI.hand.append(pile.pop())
            for i in range(3):
                AI.hand.append(deck.pop())
            
            print "Drew {}".format(AI.hand[-4:])
            AI.coins -= 1 
        
        elif buy_one < 0.2 and buy_two > 0.9 and AI.coins > 1 and not AI.down:
            
            AI.hand.append(pile.pop())
            AI.hand.append(pile.pop())
            for i in range(6):
                AI.hand.append(deck.pop())
            print "Drew {}".format(AI.hand[-8:])
            AI.coins -= 2 
        else:
            AI.hand.append(deck.pop())
            print "Drew {}".format(AI.hand[-1:])
        
        
        pile.append(deck.pop())
        toss = AI.play(check_playable(AI.hand, n, s))
        deck.insert(0, toss)
        if len(pile) > 4:
            deck.insert(0, pile.pop(0))
        
        if AI.down:
            n=1
            s=3
        

