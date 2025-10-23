from training.util.classes import GameHistory, Player, State
from training.util.playing import play_round
from training.util.helpers import get_reward, get_actions, get_states
from training.agents.agent import Agent, register_agent

from typing import List, Callable, Type
from prettytable import PrettyTable
import random
import ast

@register_agent
class TabularAgent(Agent):

    def __init__(self, k : int):
        super().__init__(k)
        states = get_states(k)
        self.q = {(s, a): 0 for s in states for a in get_actions(k, s)}

    def play(self, game_history: GameHistory, args : dict):
        action = self.get_greedy_action(game_history)
        return action
    
    def _serialize(self, params : dict):
        return {
            "q": {
                str(([card for card in state.get_cards(0)] + [card for card in state.get_cards(1)], action)): value
                for (state, action), value in self.q.items()
            },
            "k": self.k,
            "params": params
        }

    @classmethod
    def _deserialize(cls : Type["TabularAgent"], payload : dict) -> tuple["Agent", dict]:
        k = payload["k"]
        params = payload.get("params", {})
        agent = cls(k)
        agent.q = {}
        for key, value in payload["q"].items():
            card_values, action_value = ast.literal_eval(key)
            p0_cards, p1_cards = tuple(c for c in card_values[:len(card_values)//2]), tuple(c for c in card_values[len(card_values)//2:])
            state = State(p0_cards, p1_cards)
            action = action_value
            agent.q[(state, action)] = value
        return agent, params

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.choice(get_actions(self.k, game_history.get_state()))
        return self.get_greedy_action(game_history)

    def train(
            self, 
            epochs: int, 
            epsilon : float, 
            learning_rate : float, 
            discount_factor : float, 
            strategy : Callable[[Player, GameHistory], int]
    ):
        for t in range(epochs):
            print(f"Epoch {t+1}/{epochs}", end="\r")
            def agent_strategy(player: Player, game_history: GameHistory, args : dict) -> int:
                return self.play_eps_greedy(game_history, epsilon)
            game_history = play_round(self.k, agent_strategy, strategy, t)
            trajectory = game_history.get_history()
            for i in range(len(trajectory)-1):
                state, next_state = trajectory[i], trajectory[i+1]
                action = next_state.get_action(0)
                next_state_value = 0
                if not next_state.is_terminal(self.k):
                    next_action = self.get_greedy_action_by_state(next_state)
                    next_state_value = self.q[(next_state, next_action)]
                reward = get_reward(next_state)
                self.q[(state, action)] += learning_rate * (reward + discount_factor * next_state_value - self.q[(state, action)])

    def get_greedy_action(self, game_history: GameHistory):
        state = game_history.get_state()
        return self.get_greedy_action_by_state(state)
    
    def get_greedy_action_by_state(self, state: State):
        actions = get_actions(self.k, state)
        q_values = [self.q[(state, a)] for a in actions]
        max_q = max(q_values)
        max_actions = [a for (a, q) in zip(actions, q_values) if q == max_q]
        return random.choice(max_actions)
    
    def print_q(self):
        table = PrettyTable()
        table.field_names = ["State", "Action", "Q-Value"]
        table.align["State"] = "l"
        table.align["Action"] = "c"  
        table.align["Q-Value"] = "r" 
        for ((state, action), val) in self.q.items():
            table.add_row([state, action, f"{val:.3f}"])
        print(table)