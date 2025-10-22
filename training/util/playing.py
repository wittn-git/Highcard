from training.util.classes import Player, Card, GameHistory

from typing import Callable, List
import copy

def play_trick(player_1 : Player, player_2 : Player, game_history : GameHistory, round : int, show: bool = False):
    args = {"round": round}
    card_1 = player_1.play(game_history, args)
    card_2 = player_2.play(game_history, args)
    if show:
        print(card_1, card_2)
    game_history.add_record(card_1, card_2)

def play_round(
        starting_cards : List[Card], 
        strategy_1 : Callable[[Player, GameHistory], Card], 
        strategy_2 : Callable[[Player, GameHistory], Card],
        round : int = 0,
        show: bool = False
    ):
    
    player_1 = Player(id=0, starting_cards=copy.deepcopy(starting_cards), play_func=strategy_1)
    player_2 = Player(id=1, starting_cards=copy.deepcopy(starting_cards), play_func=strategy_2)
    game_history = GameHistory()

    for _ in range(len(starting_cards)):
        play_trick(player_1, player_2, game_history, round, show)
        
    return game_history

def play_rounds(
        n_rounds : int, 
        starting_cards : List[Card], 
        strategy_1 : Callable[[Player, GameHistory], Card], 
        strategy_2 : Callable[[Player, GameHistory], Card]
    ):
    
    wins_0, wins_1, draws = 0, 0, 0

    wins_per_strat = {i: 0 for i in range(4)}
    loses_per_strat = {i: 0 for i in range(4)}
    draws_per_strat = {i: 0 for i in range(4)}

    for i in range(n_rounds):

        game_history = play_round(starting_cards, strategy_1, strategy_2, i)
        winner = game_history.winner()

        if winner == 0: 
            wins_0 += 1
            wins_per_strat[i%4] +=1
        elif winner == 1: 
            wins_1 += 1
            loses_per_strat[i%4] +=1
        else: 
            draws += 1
            draws_per_strat[i%4] +=1
    
    print(wins_per_strat)
    print(loses_per_strat)
    print(draws_per_strat)

    return wins_0, wins_1, draws