from typing import List, Callable, Tuple
from itertools import product
import copy

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

class State:

    def __init__(self, cards_p0 : Tuple[Card], cards_p1: Tuple[Card]):
        self.cards_p0 = cards_p0
        self.cards_p1 = cards_p1
    
    def add_cards(self, card_p0 : Card, card_p1 : Card):
        self.cards_p0 += (card_p0,)
        self.cards_p1 += (card_p1,)
    
    def get_ncards(self) -> int:
        return len(self.cards_p0)

    def get_trick_winner(self, index : int = -1) -> int:
        if self.cards_p0[index] > self.cards_p1[index]:
            return 0
        elif self.cards_p1[index] > self.cards_p0[index]:
            return 1
        return -1
    
    def get_game_winner(self) -> int:
        score_p0, score_p1 = 0, 0
        for i in range(len(self.cards_p0)):
            winner = self.get_trick_winner(i)
            if winner == 0: score_p0 += 1
            elif winner == 1: score_p1 += 1
        if score_p0 > score_p1: return 0
        elif score_p1 > score_p0: return 1
        return -1
    
    def get_cards(self, player_id: int) -> Tuple[Card]:
        if player_id == 0:
            return self.cards_p0
        elif player_id == 1:
            return self.cards_p1
        raise ValueError("Invalid player ID")
    
    def get_action(self, player_id : int, index : int = -1) -> Card:
        if player_id == 0:
            return self.cards_p0[index]
        elif player_id == 1:
            return self.cards_p1[index]
        raise ValueError("Invalid player ID")

    def __hash__(self):
        return hash((self.cards_p0, self.cards_p1))
    
    def __repr__(self):
        if not self.cards_p0 and not self.cards_p1:
            return "State()"
        repr = "State("
        for card_p0, card_p1 in zip(self.cards_p0, self.cards_p1):
            repr += f"({card_p0}, {card_p1}), "
        repr = repr[:-2] + ")"
        return repr

    def __eq__(self, value):
        if not isinstance(value, State):
            return False
        return self.cards_p0 == value.cards_p0 and self.cards_p1 == value.cards_p1

class GameHistory:

    def __init__(self):
        self.history = [State((), ())]

    def add_record(self, card_p0 : Card, card_p1 : Card):
        last_state = copy.deepcopy(self.history[-1])
        last_state.add_cards(card_p0, card_p1)
        self.history.append(last_state)

    def get_history(self) -> List[State]:
        return self.history

    def get_state(self) -> State:
        return self.history[-1]

    def winner(self) -> int:
        return self.history[-1].get_game_winner()

class Player:

    def __init__(self, id: int, starting_cards : List[Card], play_func: Callable[["Player", GameHistory], Card]):
        self.id = id
        self.cards = starting_cards
        self._play_func = play_func
    
    def play(self, game_history: GameHistory) -> Card:
        selected_card = self._play_func(self, game_history)
        self.cards.remove(selected_card)
        return selected_card

def get_states(cards : List[Card]) -> List[State]:
    
    tuples = list(product(cards, repeat=2))
    states = []

    def backtrack(used_first, used_second, current_p0, current_p1):
        states.append(State(tuple(current_p0), tuple(current_p1)))
        for (a, b) in tuples:
            if a not in used_first and b not in used_second:
                backtrack(used_first | {a}, used_second | {b}, current_p0 + [a], current_p1 + [b])

    backtrack(set(), set(), [], [])
    
    return states