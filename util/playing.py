from util.classes import Player, Card, GameHistory

from typing import Callable, List
import copy

def play_round(
        starting_cards : List[Card], 
        strategy_1 : Callable[[Player, GameHistory], Card], 
        strategy_2 : Callable[[Player, GameHistory], Card],
        show: bool = False
    ):
    
    player_1 = Player(id=0, starting_cards=copy.deepcopy(starting_cards), play_func=strategy_1)
    player_2 = Player(id=1, starting_cards=copy.deepcopy(starting_cards), play_func=strategy_2)
    game_history = GameHistory()

    for _ in range(len(starting_cards)):
        card_1 = player_1.play(game_history)
        card_2 = player_2.play(game_history)
        if show:
            print(card_1, card_2)
        game_history.add_record(card_1, card_2)

    return game_history

def play_rounds(
        n_rounds : int, 
        starting_cards : List[Card], 
        strategy_1 : Callable[[Player, GameHistory], Card], 
        strategy_2 : Callable[[Player, GameHistory], Card]
    ):
    
    wins_0, wins_1, draws = 0, 0, 0

    for _ in range(n_rounds):

        game_history = play_round(starting_cards, strategy_1, strategy_2)
        winner = game_history.winner()

        if winner == 0: wins_0 += 1
        elif winner == 1: wins_1 += 1
        else: draws += 1

    return wins_0, wins_1, draws