from util.classes import Player, GameHistory, Card
import random

random.seed(42)

def random_strategy(player: Player, game_history: GameHistory) -> Card:
    selected_card = random.choice(player.cards)
    return selected_card

def highest_card_strategy(player: Player, game_history: GameHistory) -> Card:
    selected_card = max(player.cards, key=lambda card: card.value)
    return selected_card