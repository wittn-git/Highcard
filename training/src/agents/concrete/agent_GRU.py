from training.src.game.classes import Player, State, StateHistory
from training.src.game.playing import play_trick
from training.src.learning.gru_net import GRUNet
from training.src.other.replay_buffer import ReplayBuffer
from training.src.game.game_helpers import get_reward, get_actions, get_states
from training.src.agents.abstract.agent import register_agent, Agent
from training.src.agents.concrete.agent_STRAT import StrategyAgent

from typing import Type
import numpy as np
import random
import torch

@register_agent
class GRUAgent(Agent):

    def __init__(self, k: int, layer_n : int, hidden_sizes: int):
        super().__init__(k)
        self.model = GRUNet(input_shape=k*2, output_shape=k, hidden_sizes=hidden_sizes)
        self.layer_n, self.hidden_sizes = layer_n, hidden_sizes
        self.hidden_state = None
    
    # Serialization methods

    def _serialize(self, params: dict) -> dict:
        # Convert tensor values to lists for JSON serialization
        state_dict = self.model.state_dict()
        serializable_state_dict = {k: v.tolist() for k, v in state_dict.items()}
        return {
                    "model_state_dict": serializable_state_dict,
                    "k": self.k,
                    "hidden_sizes": self.hidden_sizes,
                    "layer_n": self.layer_n,
                    "params": params
            }

    @classmethod
    def _deserialize(cls: Type["GRUAgent"], payload: dict) -> tuple["Agent", dict]:
        k = payload["k"]
        layer_n = payload["layer_n"]
        hidden_sizes = payload["hidden_sizes"]
        params = payload.get("params", {})
        agent = cls(k, layer_n, hidden_sizes)
        state_dict = {k: torch.tensor(v) for k, v in payload["model_state_dict"].items()}
        agent.model.load_state_dict(state_dict)
        return agent, params
    
    # Playing methods

    def play(self, cards : list[int], state_history: StateHistory, player_id : int, args: dict) -> int:
        state = state_history.top(player_id)
        return self.get_greedy_action(state)
    
    def play_eps_greedy(self, state: State, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.choice(get_actions(self.k, state))
        return self.get_greedy_action(state)

    def get_greedy_action(self, state: State) -> int:
        input = self.transform_state_to_input(state)
        q_values = self.model.apply(input, self.hidden_state)
        return self.get_best_action(state, q_values)[0]
    
    # Training method
    
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
        # TODO implement
        pass
    
    def name(self):
        return "gru"