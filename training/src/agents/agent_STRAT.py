from training.src.game.classes import GameHistory, Player
from training.src.agents.agent import Agent, register_agent
from training.src.game.strategies import *

from typing import List, Callable, Type
import importlib

@register_agent
class StrategyAgent(Agent):

    def __init__(self, k : int, strategy : Callable[[Player, GameHistory], int]):
        super().__init__(k)
        self.strategy = strategy

    def play(self, game_history: GameHistory, args : dict):
        player = Player(args["player_id"], self.k, self.strategy)
        player.cards = game_history.get_state().get_residual_cards(args["player_id"], self.k)
        return self.strategy(player, game_history, args)
    
    def _serialize(self, params : dict):
        return {
            "strategy": self.strategy.__name__,
            "k": self.k,
            "params": params
        }

    @classmethod
    def _deserialize(cls : Type["StrategyAgent"], payload : dict) -> tuple["Agent", dict]:
        k = payload["k"]
        params = payload.get("params", {})
        strategy_name = payload["strategy"]
        mod = importlib.import_module("training.util.strategies")
        strategy = getattr(mod, strategy_name) 
        agent = cls(k, strategy)
        return agent, params