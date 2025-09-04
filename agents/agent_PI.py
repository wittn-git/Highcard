from util.classes import Card, GameHistory, Player
from util.playing import play_round
from util.helpers import is_terminal, get_reward, get_actions, get_states
from agents.agent import Agent

from typing import List, Tuple, Callable
from itertools import product
from prettytable import PrettyTable
import random

class TabularAgent(Agent):

    def __init__(self, starting_cards : List[Card]):
        super().__init__(starting_cards)
        states = get_states(starting_cards)
        self.q = {(s, a): 0 for s in states for a in get_actions(starting_cards, s)}
    
    def play(self, game_history: GameHistory):
        state = game_history.get_state()
        action = self.get_greedy_action(state)
        return action

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> Card:
        if random.random() < epsilon:
            return random.choice(get_actions(self.starting_cards, game_history.get_state()))
        state = game_history.get_state()
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
            for i in range(len(trajectory)-1):
                state, next_state = trajectory[i], trajectory[i+1]
                action = next_state.get_action(0)
                next_state_value = 0
                if not is_terminal(self.starting_cards, next_state):
                    next_action = self.get_greedy_action(next_state)
                    next_state_value = self.q[(next_state, next_action)]
                reward = get_reward(next_state)
                self.q[(state, action)] += learning_rate * (reward + discount_factor * next_state_value - self.q[(state, action)])
    
    def get_greedy_action(self, state):
        actions = get_actions(self.starting_cards, state)
        q_values = [self.q[(state, a)] for a in actions]
        max_q = max(q_values)
        max_actions = [a for (a, q) in zip(actions, q_values) if q == max_q]
        return random.choice(max_actions)
    
    def print_q(self):
        table = PrettyTable()
        table.field_names = ["State", "Action", "Q-Value"]
        table.align = "l"
        for ((s, a), val) in self.q.items():
            table.add_row([s, a, val])
        print(table)