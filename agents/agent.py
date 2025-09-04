from util.classes import Card, GameHistory

from typing import List
from abc import ABC, abstractmethod

class Agent(ABC):

    def __init__(self, starting_cards : List[Card]):
        self.starting_cards = starting_cards

    def get_strategy(self):
        strategy = lambda player, game_history: self.play(game_history)
        return strategy

    @abstractmethod
    def play(self, game_history: GameHistory):
        pass