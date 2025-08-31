from typing import List, Callable, Tuple

class Card:
    def __init__(self, value : int):
        self.value = value

    def __gt__(self, other : "Card"):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value > other.value
    
    def __eq__(self, other : "Card"):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __repr__(self):
        return f"Card({self.value})"

class GameHistory:

    def __init__(self):
        self.history = []

    def add_record(self, card_p0 : Card, card_p1 : Card):
        self.history.append((card_p0, card_p1))

    def get_history(self) -> Tuple[Tuple[Card, Card]]:
        return tuple(self.history)

    def winner(self) -> int:
        score_p0, score_p1 = 0, 0
        for card_p0, card_p1 in self.history:
            if card_p0 > card_p1:
                score_p0 += 1
            elif card_p1 > card_p0:
                score_p1 += 1
        if score_p0 > score_p1: return 0
        elif score_p1 > score_p0: return 1
        return -1

class Player:

    def __init__(self, id: int, starting_cards : List[Card], play_func: Callable[["Player", GameHistory], Card]):
        self.id = id
        self.cards = starting_cards
        self._play_func = play_func
    
    def play(self, game_history: GameHistory) -> Card:
        selected_card = self._play_func(self, game_history)
        self.cards.remove(selected_card)
        return selected_card