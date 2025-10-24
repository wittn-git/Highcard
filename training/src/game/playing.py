from training.src.game.classes import Player, GameHistory

from typing import Callable

def play_trick(player_1 : Player, player_2 : Player, game_history : GameHistory, show: bool = False):
    card_1 = player_1.play(game_history, {"player_id": 0})
    card_2 = player_2.play(game_history, {"player_id": 0})
    if show:
        print(card_1, card_2)
    game_history.add_record(card_1, card_2)

def play_round(
        k : int, 
        strategy_1 : Callable[[Player, GameHistory], int], 
        strategy_2 : Callable[[Player, GameHistory], int],
        show: bool = False
    ):
    
    player_1 = Player(id=0, k=k, play_func=strategy_1)
    player_2 = Player(id=1, k=k, play_func=strategy_2)
    game_history = GameHistory()

    for _ in range(k):
        play_trick(player_1, player_2, game_history, show)
        
    return game_history

def play_rounds(
        n_rounds : int, 
        k : int, 
        strategy_1 : Callable[[Player, GameHistory], int], 
        strategy_2 : Callable[[Player, GameHistory], int]
    ):
    
    wins_0, wins_1, draws = 0, 0, 0

    for _ in range(n_rounds):

        game_history = play_round(k, strategy_1, strategy_2)
        winner = game_history.winner()

        if winner == 0: 
            wins_0 += 1
        elif winner == 1: 
            wins_1 += 1
        else: 
            draws += 1

    return wins_0, wins_1, draws