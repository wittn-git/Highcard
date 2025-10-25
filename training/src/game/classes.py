from typing import List, Callable, Tuple

class State:

    def __init__(self, k : int, cards_p0: Tuple[int] = (), cards_p1: Tuple[int] = ()):
        if not isinstance(k, int):
            raise TypeError(f"State.__init__: expected int for k, got {type(k).__name__}")
        self.k = k
        self.cards_p0 = cards_p0
        self.cards_p1 = cards_p1
    
    def add_cards(self, card_p0: int, card_p1: int):
        self.cards_p0 += (card_p0,)
        self.cards_p1 += (card_p1,)
    
    def get_predecessor(self):
        return State(self.k, self.cards_p0[:-1], self.cards_p1[:-1])
    
    def get_successor(self, card_p0: int, card_p1: int):
        return State(self.k, self.get_cards(0) + (card_p0, ), self.get_cards(1) + (card_p1, ))
    
    def empty(self):
        return len(self.cards_p0) == 0
    
    def get_ncards(self) -> int:
        return len(self.cards_p0)

    def get_trick_winner(self, index: int = -1) -> int:
        if self.cards_p0[index] > self.cards_p1[index]:
            return 0
        elif self.cards_p1[index] > self.cards_p0[index]:
            return 1
        return -1
    
    def get_scores(self) -> tuple[int, int]:
        score_p0, score_p1 = 0, 0
        for i in range(len(self.cards_p0)):
            winner = self.get_trick_winner(i)
            if winner == 0: score_p0 += 1
            elif winner == 1: score_p1 += 1
        return score_p0, score_p1
    
    def get_winner(self) -> int:
        score_p0, score_p1 = self.get_scores()
        if score_p0 > score_p1: return 0
        elif score_p1 > score_p0: return 1
        return -1
    
    def get_cards(self, player_id: int) -> Tuple[int]:
        if player_id == 0:
            return self.cards_p0
        elif player_id == 1:
            return self.cards_p1
        raise ValueError("Invalid player ID")
    
    def get_residual_cards(self, player_id: int) -> Tuple[int]:
        player_card_set = set(self.get_cards(player_id))
        starting_card_set = set([i for i in range(self.k)])
        return tuple(starting_card_set - player_card_set)
    
    def get_action(self, player_id: int, index: int = -1) -> int:
        if player_id == 0:
            return self.cards_p0[index]
        elif player_id == 1:
            return self.cards_p1[index]
        raise ValueError("Invalid player ID")
    
    def get_trajectory(self) -> List["State"]:
        trajectory = []
        current_state = self.copy()
        while not current_state.empty():
            trajectory.append(current_state)
            current_state = current_state.get_predecessor()
        trajectory.append(current_state)
        trajectory.reverse()
        return trajectory
    
    def is_terminal(self) -> bool:
        return self.get_ncards() == self.k
    
    def copy(self) -> "State":
        return State(self.k, self.cards_p0, self.cards_p1)

    def __hash__(self) -> int:
        return hash((self.cards_p0, self.cards_p1))
    
    def __repr__(self) -> str:
        if self.empty():
            return f"State(k={self.k})[]"
        repr = f"State(k={self.k})["
        for card_p0, card_p1 in zip(self.cards_p0, self.cards_p1):
            repr += f"({card_p0}, {card_p1}), "
        repr = repr[:-2] + "]"
        return repr

    def __eq__(self, value):
        if not isinstance(value, State):
            return False
        return self.cards_p0 == value.cards_p0 and self.cards_p1 == value.cards_p1

class StateHistory:
    
    def __init__(self, k : int, state: State = None):
        self.history: List[State] = [State(k)]
        if state is not None:
            self.push(state)
    
    def push(self, state: State):
        if not self.is_empty() and not self.top().is_terminal():
            self.history.pop()
        self.history.append(state)
    
    def pop(self) -> State:
        return self.history.pop()
    
    def is_terminal(self) -> bool:
        if self.is_empty():
            return False
        return self.top().is_terminal()
    
    def top(self) -> State:
        return self.history[-1]
    
    def is_empty(self) -> bool:
        return len(self.history) == 0
    
    def __repr__(self) -> str:
        repr = "StateHistory[\n"
        for state in self.history:
            repr += f"  {state}\n"
        repr += "]"
        return repr
    
class Player:

    def __init__(self, id: int, k: int, play_func: Callable[["Player", StateHistory], int], cards: list[int] = None):
        self.id = id
        self.k = k
        self._play_func = play_func
        self.cards = cards if cards is not None else list(range(self.k))
    
    def play(self, state_history: StateHistory, args: dict) -> int:
        selected_card = self._play_func(self, state_history, args)
        self.cards.remove(selected_card)
        return selected_card

    def reset(self):
        self.cards = [i for i in range(self.k)]