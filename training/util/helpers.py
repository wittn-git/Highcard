from util.classes import Card, State

from typing import Tuple, List
from itertools import product

def is_terminal(starting_cards: List[Card], state: State) -> bool:
    return state.get_ncards() == len(starting_cards)

def get_reward(state: Tuple[Tuple[Card, Card]]) -> float:
    trick_winner = state.get_trick_winner()
    if trick_winner == 0:
        return 1.0
    elif trick_winner == 1:
        return -1.0
    return 0.0

def get_actions(starting_cards : List[Card], state: State) -> List[Card]:
    playable_cards = starting_cards.copy()
    played_cards = state.get_cards(0)
    for card in starting_cards:
        if card in played_cards:
            playable_cards.remove(card)
    return playable_cards

def get_states(cards : List[Card]) -> List[State]:

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