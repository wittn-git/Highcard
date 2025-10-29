from training.src.game.classes import Player, State, StateHistory
from training.src.game.playing import play_round
from training.src.game.game_helpers import get_reward, get_actions, get_states
from training.src.agents.abstract.agent import Agent, register_agent
from training.src.agents.concrete.agent_STRAT import StrategyAgent
from training.src.util.seeding import seed_rnd

from typing import Type
from prettytable import PrettyTable
import random
import ast

@register_agent
class TabularAgent(Agent):

    def __init__(self, k: int):
        super().__init__(k)
        states = get_states(k)
        self.q = {(s, a): 0 for s in states for a in get_actions(k, s)}

    def play(self, cards : list[int], state_history: StateHistory, player_id : int, args: dict) -> int:
        state = state_history.top(player_id)
        return self.get_greedy_action(state)
    
    def _serialize(self, params: dict) -> dict:
        return {
            "q": {
                str(([card for card in state.get_cards(0)] + [card for card in state.get_cards(1)], action)): value
                for (state, action), value in self.q.items()
            },
            "k": self.k,
            "params": params
        }

    @classmethod
    def _deserialize(cls: Type["TabularAgent"], payload: dict) -> tuple["Agent", dict]:
        k = payload["k"]
        params = payload.get("params", {})
        agent = cls(k)
        agent.q = {}
        for key, value in payload["q"].items():
            card_values, action_value = ast.literal_eval(key)
            p0_cards, p1_cards = tuple(c for c in card_values[:len(card_values)//2]), tuple(c for c in card_values[len(card_values)//2:])
            state = State(k, p0_cards, p1_cards)
            action = action_value
            agent.q[(state, action)] = value
        return agent, params

    def play_eps_greedy(self, state: State, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.choice(get_actions(self.k, state))
        return self.get_greedy_action(state)

    def train(
            self, 
            epochs: int, 
            epsilon: float, 
            learning_rate: float, 
            discount_factor: float, 
            seed : int,
            adversarial_agent: Agent
    ):  
        seed_rnd(seed)
        state_history = StateHistory(self.k)
        def agent_strategy(cards : list[int], state_history: StateHistory, player_id : int, args: dict) -> int:
                return self.play_eps_greedy(state_history.top(), epsilon)
        player_0, player_1 = Player(0, self.k, StrategyAgent(self.k, agent_strategy)), Player(1, self.k, adversarial_agent)
        for t in range(epochs):
            print(f"Epoch {t+1}/{epochs}", end="\r")
            state_history = play_round(self.k, player_0, player_1, state_history)
            trajectory = state_history.top().get_trajectory()
            for i in range(len(trajectory)-1):
                state, next_state = trajectory[i], trajectory[i+1]
                action = next_state.get_action(0)
                next_state_value = 0
                if not next_state.is_terminal():
                    next_action = self.get_greedy_action(next_state)
                    next_state_value = self.q[(next_state, next_action)]
                reward = get_reward(next_state)
                self.q[(state, action)] += learning_rate * (reward + discount_factor * next_state_value - self.q[(state, action)])
    
    def get_greedy_action(self, state: State) -> int:
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

    def name(self) -> str:
        return "tabular"