from training.src.game.classes import State

from typing import Tuple, List
from itertools import product

def get_reward(state: Tuple[Tuple[int, int]]) -> float:
    trick_winner = state.get_trick_winner()
    if trick_winner == 0:
        return 1.0
    elif trick_winner == 1:
        return -1.0
    return 0.0

def get_actions(k : int, state: State) -> List[int]:
    playable_cards = set([i for i in range(k)])
    played_cards = set(state.get_cards(0))
    return list(playable_cards - played_cards)

def get_states(k : int) -> List[State]:

    cards = [i for i in range(k)]
    tuples = list(product(cards, repeat=2))
    states = []

    def backtrack(used_first, used_second, current_p0, current_p1):
        
        current_state = State(tuple(current_p0), tuple(current_p1))
        states.append(current_state)
        
        if len(used_first) >= len(cards) - 1: return
            
        for (a, b) in tuples:
            if a not in used_first and b not in used_second:
                backtrack(used_first | {a}, used_second | {b}, current_p0 + [a], current_p1 + [b])

    backtrack(set(), set(), [], [])
    
    return states