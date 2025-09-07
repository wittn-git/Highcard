from util.classes import Card, GameHistory, Player, State
from util.playing import play_trick
from util.neural_nets import NeuralNetwork
from util.replay_buffer import ReplayBuffer
from util.helpers import is_terminal, get_reward, get_actions, get_states
from agents.agent import Agent, register_agent

from typing import List, Tuple, Callable, Type
from itertools import product
import random
from prettytable import PrettyTable

@register_agent
class DQNAgent:

    def __init__(self, starting_cards : List[Card]):
        super().__init__(starting_cards)
        self.model = NeuralNetwork(input_size=len(starting_cards)*2, output_size=len(starting_cards))

    def play(self, game_history: GameHistory):
        action = self.get_greedy_action(game_history)
        return action
    
    def _serialize(self):
        return {
                    "model_state_dict": self.model.state_dict(),
                    "starting_cards": [c.value for c in self.starting_cards]
            }

    @classmethod
    def _deserialize(cls : Type["DQNAgent"], payload : dict):
        starting_cards = [Card(c) for c in payload["starting_cards"]]
        agent = cls(starting_cards)
        agent.model.load_state_dict(payload["model_state_dict"])
        return agent

    def transform_state_to_input(self, state: State) -> List[float]:
        input = [card.value for card in state.get_cards(0)] + [card.value for card in state.get_cards(1)]
        return input
    
    def transform_output_to_action(self, output: List[float], state: State) -> Card:
        valid_actions = state.get_cards(0)
        valid_action_indices = [card.value for card in valid_actions]
        best_action_index = max(valid_action_indices, key=lambda idx: output[idx])
        return Card(best_action_index)

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> Card:
        if random.random() < epsilon:
            return random.choice(get_actions(self.starting_cards, game_history.get_state()))
        return self.get_greedy_action(game_history)

    def get_greedy_action(self,  game_history: GameHistory) -> Card:
        state = game_history.get_state()
        input = self.transform_state_to_input(state)
        output = self.model.forward(input)
        action = self.transform_output_to_action(output, state)
        return action

    def train(
            self, 
            epochs: int, 
            epsilon : float, 
            learning_rate : float, 
            discount_factor : float, 
            replay_buffer_capacity : int,
            strategy : Callable[[Player, GameHistory], Card]
    ):  
        game_history = GameHistory()
        replay_buffer = ReplayBuffer(capacity=replay_buffer_capacity)
        for t in range(epochs):
            if is_terminal(self.starting_cards, game_history.get_state()):
                game_history = GameHistory()
            action = self.play_eps_greedy(game_history, epsilon)
            state = game_history.get_state()
            # add (s, a, r, s', done) to replay buffer
            # sample minbatch from replay buffer
            # for each element in minibatch:
            #   compute target: if done: target = r else: target = r + discount_factor * max_a' Q(s', a') (fixed weights)
            #   do gradient step on (target - Q(s, a))^2
            # if t % update_steps == 0: update fixed weights