import random, logging
from collections import Counter

from flask import Flask, session, request, render_template, jsonify

from app.util import unflatten
from app.fiftycents import FiftyCentsGame
from app.fiftycents import Card

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = 'peanut'
game = FiftyCentsGame(2)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        data = unflatten(request.form.to_dict())
        for k,v in data["play"].items():
            data["play"][k] = int(v)
        game.play(data)
    
    player = {"hand": {k: 0 for k in Card.RANKS}, 
              "coins": game.player.coins,
              "points": game.player.total_score}
        
    for k, v in dict(Counter([c.rank for c in game.player.hand])).items():
        player["hand"][k] = v
    
    goal = {"set_num":  game.current_round[0],
            "set_size": game.current_round[1]}
    
    pile = [c.rank for c in game.open_deck.cards]
        
    return render_template('main.html', 
                           player=player, 
                           pile=pile, 
                           goal=goal,
                           playable = sorted([c for c in game.cards_in_play if c not in ["2", "JOKER"]]), 
                           player_has_drawn=game.player_has_drawn,
                           game_over = game.game_over,
                           player_score = game.player.get_current_score(),
                           ai_score = game.AI.get_current_score(),
                           ai_total = game.AI.total_score)
    
@app.route("/info/", methods=['GET'])
def info():
    return jsonify({"player": {
                        "hand": [c.rank for c in game.player.hand],
                        "played": [c.rank for c in game.player.played_cards],
                        "coins": game.player.coins,
                        "score": game.player.get_current_score()
                        },
                    "computer": {
                        "hand": [c.rank for c in game.AI.hand],
                        "played": [c.rank for c in game.AI.played_cards],
                        "coins": game.AI.coins,
                        "score": game.AI.get_current_score()
                        },
                    "game": {
                        "open": [c.rank for c in game.open_deck.cards],
                        "cards_in_play": list(game.cards_in_play),
                        "round": game.current_round
                        }
                    })
