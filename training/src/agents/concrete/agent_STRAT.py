from training.src.game.classes import Player, StateHistory
from training.src.agents.abstract.agent import Agent, register_agent
from training.src.game.strategies import *

from typing import List, Callable, Type
import importlib

@register_agent
class StrategyAgent(Agent):

    def __init__(self, k: int, strategy: Callable[[Player, StateHistory], int]):
        super().__init__(k)
        self.strategy = strategy

    def play(self, cards : list[int], state_history: StateHistory, player_id : int, args: dict) -> int:
        return self.strategy(cards, state_history, player_id, args)
    
    def _serialize(self, params: dict):
        return {
            "strategy": self.strategy.__name__,
            "k": self.k,
            "params": params
        }

    @classmethod
    def _deserialize(cls: Type["StrategyAgent"], payload: dict) -> tuple["Agent", dict]:
        k = payload["k"]
        params = payload.get("params", {})
        strategy_name = payload["strategy"]
        mod = importlib.import_module("training.src.game.strategies")
        strategy = getattr(mod, strategy_name) 
        agent = cls(k, strategy)
        return agent, params
    
    def name(self) -> str:
        return "strat-" + self.strategy.__name__.replace("_strategy", "")