from util.classes import Card, GameHistory, Player
from util.playing import play_round
from util.neural_nets import NeuralNetwork
from agents.agent import Agent, register_agent

from typing import List, Tuple, Callable
from itertools import product
import random
from prettytable import PrettyTable

@register_agent
class DQNAgent:

    def __init__(self, starting_cards : List[Card]):
        super().__init__(starting_cards)

    def play(self, game_history: GameHistory):
        state = game_history.get_state()
        action = self.model.forward(state).argmax().item()
        return action