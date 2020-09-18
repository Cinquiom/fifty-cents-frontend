from flask import flash

from app.fiftycents.entities.player import Player
from app.fiftycents.entities.deck import Deck
from app.fiftycents.entities.card import Card
from app.fiftycents.fcai.ai import FiftyCentsAI

class NotEnoughOpenCardsError(Exception): pass
class BadTossArgumentsError(Exception): pass

class FiftyCentsGame():
    
    INITIAL_HAND_SIZE = 11
    ROUNDS = iter([(1,3),
                  (2,3),
                  (1,3),
                  (2,4),
                  (1,5),
                  (2,5),
                  (1,6),
                  (2,6)])
    
    def __init__(self, deck_size):
        self.player = Player()
        self.AI = FiftyCentsAI(5000)
        
        self.deck_size = deck_size
        
        self.players_turn = True
        self.player_has_drawn = False
        self.game_over = False
        self.round_over = False;
        
        self.init_round()
        
    @property
    def cards_in_play(self):
        return set([c.rank for c in self.AI.played_cards] + [c.rank for c in self.player.played_cards] + ["2", "JOKER"])
        
    def init_round(self):
        try:
            self.current_round = next(self.ROUNDS)
        except StopIteration:
            self.game_over = True
            return
        
        self.closed_deck = Deck(self.deck_size) 
        self.open_deck = Deck(empty=True)
        self.open_deck.cover(self.closed_deck.draw())
        
        self.player.played_cards = []
        self.AI.played_cards = []

        self.player_bought = set()
        for i in range(self.INITIAL_HAND_SIZE):
            self.player.add_card(self.closed_deck.draw())
            
        for i in range(self.INITIAL_HAND_SIZE):
            self.AI.add_card(self.closed_deck.draw())
            
        print("Starting round.")
        print("Goal: Get {} set{} of {}".format(self.current_round[0],
                                                's' if self.current_round[0] > 1 else '',
                                                self.current_round[1]))
        print("")
        
        self.round_over = False
        
    def play(self, data):       
        try:
            if self.do_player_turn(data["action"], data):
                self.players_turn = False
                self.do_computer_turn(self.player_bought)
                self.players_turn = True
        except BadTossArgumentsError:
            pass
        
        if self.round_over:
            self.player.total_score += self.player.get_current_score()
            self.AI.total_score += self.AI.get_current_score()
            self.init_round()
        
        return None
                
                
    def do_player_turn(self, action, data):
        action = action.lower()
        set_num = self.current_round[0]
        set_size = self.current_round[1]
        
        if not self.player_has_drawn:
            
            if action == "buy":
                self.buy(self.player, int(data['buyamount']))
            elif action == "draw":
                self.draw(self.player)

            
            self.player_has_drawn = True
            
            return False
        
        else:
            
            
            if action == "play":
                self.play_hand(self.player, data['play'])
            elif action == "toss":
                tossme = [k for k, v in data['play'].items() if v==1]
                if len(tossme) != 1: raise BadTossArgumentsError
                
                card = self.player.toss(tossme[0])
                self.open_deck.cover(card)
                self.player_has_drawn = False
                
            if not self.player.hand:
                self.round_over = True
                return False
            elif action =="toss":
                return True
            
            return False
            
    def do_computer_turn(self, bought_card):
        n = self.current_round[0]
        s = self.current_round[1]
        
        if self.AI.down:
            n = 1
            s = 3
            
        for c in bought_card:
            self.AI.player_bought.add(c)
        
        print "Starting round for {} sets of {}".format(n,s)
        print "{} coins remaining".format(self.AI.coins)
        
        draw    = self.AI.get_draw_heuristics(0,n,s,pile=self.open_deck.cards)
        buy_one = 0
        buy_two = 0
        
        if len(self.open_deck.cards) > 0:
            buy_one = self.AI.get_draw_heuristics(1,n,s,pile=self.open_deck.cards)
         
        if len(self.open_deck.cards) > 1:   
            buy_two = self.AI.get_draw_heuristics(2,n,s,pile=self.open_deck.cards)

        print draw, buy_one, buy_two
        
        # Only buy one if we have a really good chance of going down.
        if draw < 0.1 and buy_one > 0.8 and self.AI.coins > 0 and not self.AI.down:
            self.buy(self.AI, 1)
        elif buy_one < 0.2 and buy_two > 0.9 and self.AI.coins > 1 and not self.AI.down:
            self.buy(self.AI, 2) 
        else:
            self.draw(self.AI)
        
        
        toss = self.AI.play(self.AI.get_playable_sets(self.AI.hand, n, s), self.cards_in_play)
        
        if not self.AI.hand:
            print "Round over!"
            print "Player gets {} points".format(self.player.get_current_score())
            print "AI gets {} points".format(self.AI.get_current_score())
            self.round_over = True
            return
        
        self.open_deck.cover(toss)
                
    def draw(self, player, silent=False):
        card = self.closed_deck.draw()
        player.add_card(card)
        if self.players_turn and not silent:
            flash("You drew {}".format(card.rank))  
        
    def buy(self, player, coins):
        if len(self.open_deck.cards) < coins:
            raise NotEnoughOpenCardsError
        
        for c in range(coins):
            player.spend_coin()
            
            card = self.open_deck.draw()
            player.add_card(card)
            self.player_bought.add(card.rank)
            
            for i in range(3):
                self.draw(player, silent=True)
        if self.players_turn:      
            flash("You bought: {}".format([c.rank for c in self.player.hand[-4*coins:]]))
                
    def play_hand(self, player, hand):
        n = 1 if player.down else self.current_round[0]
        s = 3 if player.down else self.current_round[1]
        
        testhand = []
        for k,v in hand.items():
            for i in range(v):
                testhand.append(Card(k))
        
        wild_hand = list(filter(lambda a: a in ["2", "JOKER"], [x.rank for x in testhand]))
    
        instructions = player.get_playable_sets(testhand, n, s)
    
        testhand = [c.rank for c in testhand]
        result = []
        if instructions:
            self.player.down=True
            for k,v in instructions.items():
                result.append([k for x in range(v[0])] + [wild_hand.pop() for x in range(v[1])])
             
            for play in result:
                for card in play:
                    testhand.remove(card)
                    c = player.toss(card)
                    player.played_cards.append(c)
        
        if player.down:
            for card in testhand:
                if card in self.cards_in_play:
                    c = player.toss(card)
                    player.played_cards.append(c)
            
