from typing import List, Callable, Tuple
from itertools import product
import copy

class State:

    def __init__(self, cards_p0 : Tuple[int], cards_p1: Tuple[int]):
        self.cards_p0 = cards_p0
        self.cards_p1 = cards_p1
    
    def add_cards(self, card_p0 : int, card_p1 : int):
        self.cards_p0 += (card_p0,)
        self.cards_p1 += (card_p1,)
    
    def get_predecessor(self):
        return State(self.cards_p0[:-1], self.cards_p1[:-1])
    
    @staticmethod
    def get_successor(state : "State", card_p0 : int, card_p1 : int):
        return State(state.get_cards(0) + (card_p0, ), state.get_cards(1) + (card_p1, ))
    
    def empty(self):
        return len(self.cards_p0) == 0
    
    def get_ncards(self) -> int:
        return len(self.cards_p0)

    def get_trick_winner(self, index : int = -1) -> int:
        if self.cards_p0[index] > self.cards_p1[index]:
            return 0
        elif self.cards_p1[index] > self.cards_p0[index]:
            return 1
        return -1
    
    def get_game_scores(self) -> tuple[int, int]:
        score_p0, score_p1 = 0, 0
        for i in range(len(self.cards_p0)):
            winner = self.get_trick_winner(i)
            if winner == 0: score_p0 += 1
            elif winner == 1: score_p1 += 1
        return score_p0, score_p1
    
    def get_game_winner(self) -> int:
        score_p0, score_p1 = self.get_game_scores()
        if score_p0 > score_p1: return 0
        elif score_p1 > score_p0: return 1
        return -1
    
    def get_cards(self, player_id: int) -> Tuple[int]:
        if player_id == 0:
            return self.cards_p0
        elif player_id == 1:
            return self.cards_p1
        raise ValueError("Invalid player ID")
    
    def get_residual_cards(self, player_id: int, k : int) -> Tuple[int]:
        player_card_set = set(self.get_cards(player_id))
        starting_card_set = set([i for i in range(k)])
        return tuple(starting_card_set - player_card_set)
    
    def get_action(self, player_id : int, index : int = -1) -> int:
        if player_id == 0:
            return self.cards_p0[index]
        elif player_id == 1:
            return self.cards_p1[index]
        raise ValueError("Invalid player ID")
    
    def is_terminal(self, k : int):
        return self.get_ncards() == k

    def __hash__(self):
        return hash((self.cards_p0, self.cards_p1))
    
    def __repr__(self):
        if self.empty():
            return "State[]"
        repr = "State["
        for card_p0, card_p1 in zip(self.cards_p0, self.cards_p1):
            repr += f"({card_p0}, {card_p1}), "
        repr = repr[:-2] + "]"
        return repr

    def __eq__(self, value):
        if not isinstance(value, State):
            return False
        return self.cards_p0 == value.cards_p0 and self.cards_p1 == value.cards_p1

class GameHistory:

    def __init__(self, state : State = None):
        if state == None:
            self.history = [State((), ())]
            return
        reversed_history = []
        new_state = state
        while not new_state.empty():
            reversed_history.append(new_state)
            new_state = new_state.get_predecessor()
        reversed_history.append(new_state)
        self.history = list(reversed(reversed_history))

    def add_record(self, card_p0 : int, card_p1 : int):
        last_state = copy.deepcopy(self.history[-1])
        last_state.add_cards(card_p0, card_p1)
        self.history.append(last_state)

    def get_history(self) -> List[State]:
        return self.history

    def get_state(self) -> State:
        return self.history[-1]

    def winner(self) -> int:
        return self.history[-1].get_game_winner()
    
    def __repr__(self):
        stringed_history = [str(state) for state in self.history]
        return f"GameHistory[{", ".join(stringed_history)}]"

class Player:

    def __init__(self, id: int, k : int, play_func: Callable[["Player", GameHistory], int], cards : list[int] = None):
        self.id = id
        self.k = k
        self._play_func = play_func
        self.cards = cards if cards is not None else list(range(self.k))
    
    def play(self, game_history: GameHistory, args : dict) -> int:
        selected_card = self._play_func(self, game_history, args)
        self.cards.remove(selected_card)
        return selected_card

    def reset(self):
        self.cards = [i for i in range(self.k)]

def get_states(cards : List[int]) -> List[State]:
    
    tuples = list(product(cards, repeat=2))
    states = []

    def backtrack(used_first, used_second, current_p0, current_p1):
        states.append(State(tuple(current_p0), tuple(current_p1)))
        for (a, b) in tuples:
            if a not in used_first and b not in used_second:
                backtrack(used_first | {a}, used_second | {b}, current_p0 + [a], current_p1 + [b])

    backtrack(set(), set(), [], [])
    
    return states