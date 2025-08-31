from util.classes import Card, GameHistory, Player
from util.util import play_round

from typing import List, Tuple, Callable
from itertools import product
import random
from prettytable import PrettyTable

# TODO: Order functions by functionality
# TODO: Consider moving some functions elsewhere

class TabularAgent:

    def __init__(self, starting_cards : List[Card]):
        self.starting_cards = starting_cards
        states = self.get_states(starting_cards)
        self.q = {(s, a): 0 for s in states for a in self.get_actions(starting_cards, s)}

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> Card:
        if random.random() < epsilon:
            return random.choice(self.get_actions(self.starting_cards, game_history.history))
        state = game_history.get_history()
        return self.get_greedy_action(state)

    def train(
            self, 
            epochs: int, 
            epsilon : float, 
            learning_rate : float, 
            discount_factor : float, 
            strategy : Callable[[Player, GameHistory], Card]
    ):
        for _ in range(epochs):
            def agent_strategy(player: Player, game_history: GameHistory) -> Card:
                return self.play_eps_greedy(game_history, epsilon)
            game_history = play_round(self.starting_cards, agent_strategy, strategy)
            trajectory = game_history.get_history()
            for i in range(len(trajectory)):
                if i == 0:
                    state, action, next_state = (), trajectory[0][0], trajectory[0:1]
                else:
                    state, action, next_state = trajectory[0:i], trajectory[i][0], trajectory[0:i + 1]
                next_state_value = 0
                if not self.is_terminal(next_state):
                    next_action = self.get_greedy_action(next_state)
                    next_state_value = self.q[(next_state, next_action)]
                reward = self.get_reward(next_state)
                self.q[(state, action)] += learning_rate * (reward + discount_factor * next_state_value - self.q[(state, action)])

    def play(self, game_history: GameHistory):
        state = game_history.get_history()
        action = self.get_greedy_action(state)
        return action
    
    def get_greedy_action(self, state):
        actions = self.get_actions(self.starting_cards, state)
        q_values = [self.q[(state, a)] for a in actions]
        max_q = max(q_values)
        max_actions = [a for (a, q) in zip(actions, q_values) if q == max_q]
        return random.choice(max_actions)
    
    def is_terminal(self, state: Tuple[Tuple[Card, Card]]) -> bool:
        return len(state) == len(self.starting_cards)

    def get_reward(self, state: Tuple[Tuple[Card, Card]]) -> float:
        if state[-1][0] > state[-1][1]:
            return 1.0
        elif state[-1][0] < state[-1][1]:
            return -1.0
        return 0.0

    def get_strategy(self):
        strategy = lambda player, game_history: self.play(game_history)
        return strategy

    def print_q(self):
        table = PrettyTable()
        table.field_names = ["State", "Action", "Q-Value"]
        table.align = "l"  # Set all columns to left alignment
        for ((s, a), val) in self.q.items():
            table.add_row([s, a, val])
        print(table)

    def get_actions(self, starting_cards : List[Card], state: Tuple[Tuple[Card, Card]]) -> List[Card]:
        playable_cards = starting_cards.copy()
        for cards in state:
            if cards[0] in playable_cards:
                playable_cards.remove(cards[0])
        return playable_cards

    def get_states(self, cards : List[Card]) -> List[Tuple[Tuple[Card, Card]]]:

        tuples = list(product(cards, repeat=2))
        results = []

        def backtrack(used_first, used_second, current):
            results.append(tuple(current))
            for (a, b) in tuples:
                if a not in used_first and b not in used_second:
                    backtrack(used_first | {a}, used_second | {b}, current + [(a, b)])

        backtrack(set(), set(), [])
        
        return results
