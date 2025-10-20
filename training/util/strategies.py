from util.classes import Player, GameHistory, Card

import random

random.seed(42)

def random_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    selected_card = random.choice(player.cards)
    return selected_card

def highest_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    selected_card = max(player.cards, key=lambda card: card.value)
    return selected_card

def lowest_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    selected_card = min(player.cards, key=lambda card: card.value)
    return selected_card

def alternating_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    if game_history.get_state().get_ncards() % 2:
        return lowest_strategy(player, game_history, args)
    return highest_strategy(player, game_history, args)

def copying_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    state = game_history.get_state()
    if state.get_ncards() == 0:
        return highest_strategy(player, game_history, args)
    last_card_adversial = state.get_cards(0)[-1]
    if last_card_adversial in player.cards:
        return last_card_adversial
    return highest_strategy(player, game_history, args)

def fixed_pool_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    if args["round"] % 4 == 0:
        return highest_strategy(player, game_history, args)
    if args["round"] % 4 == 1:
        return lowest_strategy(player, game_history, args)
    if args["round"] % 4 == 2:
        return alternating_strategy(player, game_history, args)
    return copying_strategy(player, game_history, args)

def stochastic_pool_strategy(player: Player, game_history: GameHistory, args : dict) -> Card:
    strategies = [
        highest_strategy,
        lowest_strategy,
        alternating_strategy,
        copying_strategy
    ]
    selected_strategy = random.choice(strategies)
    return selected_strategy(player, game_history, args)
    