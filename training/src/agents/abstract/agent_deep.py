from abc import ABC, abstractmethod

from training.src.game.classes import State, StateHistory
from training.src.game.game_helpers import get_actions
from training.src.agents.abstract.agent import Agent

import numpy as np
import random
import torch

class DeepAgent(Agent, ABC):

    def __init__(self, k: int):
        super().__init__(k)

    def play(self, cards : list[int], state_history: StateHistory, player_id : int, args: dict) -> int:
        state = state_history.top(player_id)
        return self.get_greedy_action(state)

    def transform_state_to_input(self, state: State) -> torch.Tensor:
        player_0_cards, player_1_cards = state.get_cards(0), state.get_cards(1)
        p0_encoding = [1 if card in player_0_cards else 0 for card in range(self.k)]
        p1_encoding = [1 if card in player_1_cards else 0 for card in range(self.k)]
        input = p0_encoding + p1_encoding
        return torch.tensor(input, dtype=torch.float32).unsqueeze(0)

    def play_eps_greedy(self, state: State, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.choice(get_actions(self.k, state))
        return self.get_greedy_action(state)

    def get_greedy_action(self, state: State) -> int:
        input = self.transform_state_to_input(state)
        q_values = self.model.apply(input)
        return self.get_best_action(state, q_values)[0]
    
    def get_best_action(self, state: State, q_values: np.ndarray) -> int:
        actions = get_actions(self.k, state)
        action_q_values = {a: q_values[a] for a in actions}
        max_q = max(action_q_values.values())
        max_actions = [a for a, q in action_q_values.items() if q == max_q]
        return random.choice(max_actions), max_q
    
    @abstractmethod
    def train(
        self, 
        epochs: int, 
        epsilon: float, 
        learning_rate: float, 
        discount_factor: float, 
        replay_buffer_capacity: int,
        update_interval: int,
        minibatch_size: int,
        adversarial_agent: Agent,
    ):
        pass