from training.src.game.classes import Player, State

import random

random.seed(42)

def random_strategy(player: Player, state: State, args: dict) -> int:
    return random.choice(player.cards)

def highest_strategy(player: Player, state: State, args: dict) -> int:
    return max(player.cards)

def lowest_strategy(player: Player, state: State, args: dict) -> int:
    return min(player.cards)

def alternating_strategy(player: Player, state: State, args: dict) -> int:
    if state.get_ncards() % 2:
        return lowest_strategy(player, state, args)
    return highest_strategy(player, state, args)

def copying_strategy(player: Player, state: State, args: dict) -> int:
    if state.get_ncards() == 0:
        return highest_strategy(player, state, args)
    last_card_adversial = state.get_cards(0)[-1]
    if last_card_adversial in player.cards:
        return last_card_adversial
    return highest_strategy(player, state, args)

def pool_strategy(player: Player, state: State, args: dict) -> int:
    strategies = [
        highest_strategy,
        lowest_strategy,
        alternating_strategy,
        copying_strategy
    ]
    selected_strategy = random.choice(strategies)
    return selected_strategy(player, state, args)