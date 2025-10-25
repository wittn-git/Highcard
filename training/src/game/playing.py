from training.src.game.classes import Player, State, StateHistory

from typing import Callable

def play_trick(player_1: Player, player_2: Player, state_history: StateHistory, show: bool = False):
    card_1 = player_1.play(state_history, {"player_id": 0})
    card_2 = player_2.play(state_history, {"player_id": 0})
    if show:
        print(card_1, card_2)
    state = state_history.pop()
    state.add_cards(card_1, card_2)
    state_history.push(state)
    return state_history

def play_round(
        k: int, 
        strategy_1: Callable[[Player, State], int], 
        strategy_2: Callable[[Player, State], int],
        state_history: StateHistory = None,
        show: bool = False
    ) -> StateHistory:

    if state_history is None:
        state_history = StateHistory(k)
    else:
        state_history.push(State(k))
    
    player_1 = Player(id=0, k=k, play_func=strategy_1)
    player_2 = Player(id=1, k=k, play_func=strategy_2)

    for _ in range(k):
        play_trick(player_1, player_2, state_history, show)
        
    return state_history

def play_rounds(
        n_rounds: int, 
        k: int, 
        strategy_1: Callable[[Player, StateHistory], int], 
        strategy_2: Callable[[Player, StateHistory], int]
    ):
    
    wins_0, wins_1, draws = 0, 0, 0
    state_history = StateHistory(k)

    for _ in range(n_rounds):

        state_history = play_round(k, strategy_1, strategy_2)
        winner = state_history.top().get_winner()

        if winner == 0: 
            wins_0 += 1
        elif winner == 1: 
            wins_1 += 1
        else: 
            draws += 1

    return wins_0, wins_1, draws