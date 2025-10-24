from training.src.game.classes import State

from typing import Type
from abc import ABC, abstractmethod
import json

_AGENT_REGISTRY = {}

def register_agent(cls):
    _AGENT_REGISTRY[cls.__name__] = cls
    return cls

class Agent(ABC):

    def __init__(self, k: int):
        self.k = k

    def get_strategy(self):
        strategy = lambda player, state, args: self.play(state, args)
        return strategy
    
    def export_agent(self, file_path: str, params: dict):
        data = {
            "class": self.__class__.__name__,
            "payload": self._serialize(params)
        }
        with open(file_path, "w") as f:
            json.dump(data, f)

    @classmethod
    def import_agent(cls, file_path: str, k: int) -> tuple["Agent", dict]:
        with open(file_path, "r") as f:
            data = json.load(f)
        agent_class = _AGENT_REGISTRY[data["class"]]
        agent, params = agent_class._deserialize(data["payload"])
        assert agent.k == k, "Passed starting cards to no matched the agents."
        return agent, params
    
    @abstractmethod
    def _serialize(self, params: dict) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _deserialize(cls: Type["Agent"], payload: dict) -> tuple["Agent", dict]:
        pass

    @abstractmethod
    def play(self, state: State, args: dict):
        pass