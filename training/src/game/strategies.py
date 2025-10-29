from training.src.game.classes import StateHistory

import random

random.seed(42)

def random_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
    return random.choice(cards)

def highest_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
    return max(cards)

def lowest_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
    return min(cards)

def alternating_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
    state = state_history.top()
    if state.get_ncards() % 2:
        return lowest_strategy(cards, state, args)
    return highest_strategy(cards, state, args)

def copying_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
    state = state_history.top()
    if state.get_ncards() == 0:
        return highest_strategy(cards, state, args)
    last_card_adversial = state.get_cards(1-player_id)[-1]
    if last_card_adversial in cards:
        return last_card_adversial
    return highest_strategy(cards, state, args)

def pool_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
    strategies = [
        highest_strategy,
        lowest_strategy,
        alternating_strategy,
        copying_strategy
    ]
    selected_strategy = random.choice(strategies)
    return selected_strategy(cards, state_history, args)