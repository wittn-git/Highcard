from util.classes import Card, GameHistory

from typing import List, Type
from abc import ABC, abstractmethod
import json

_AGENT_REGISTRY = {}

def register_agent(cls):
    _AGENT_REGISTRY[cls.__name__] = cls
    return cls

class Agent(ABC):

    def __init__(self, starting_cards : List[Card]):
        self.starting_cards = starting_cards

    def get_strategy(self):
        strategy = lambda player, game_history, args: self.play(game_history, args)
        return strategy
    
    def export_agent(self, file_path: str):
        data = {
            "class": self.__class__.__name__,
            "payload": self._serialize()
        }
        with open(file_path, "w") as f:
            json.dump(data, f)

    @classmethod
    def import_agent(cls, file_path: str, starting_cards : list[Card]):
        with open(file_path, "r") as f:
            data = json.load(f)
        agent_class = _AGENT_REGISTRY[data["class"]]
        agent = agent_class._deserialize(data["payload"])
        assert agent.starting_cards == starting_cards, "Passed starting cards to no matched the agents."
        return agent
    
    @abstractmethod
    def _serialize(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _deserialize(cls : Type["Agent"], payload : dict):
        pass

    @abstractmethod
    def play(self, game_history: GameHistory, args : dict):
        pass