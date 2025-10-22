from training.util.classes import Card, GameHistory, Player
from training.agents.agent import Agent

from typing import Callable
import time

def get_file_name(agent : Agent, adversarial_strategy : Callable[[Player, GameHistory], Card], starting_cards : list[Card]) -> str:
    strategy_name = adversarial_strategy.__name__.replace("_", "-")
    agent_type = type(agent).__name__
    file_name = f"models/{agent_type.lower()}_{strategy_name.lower()}_{str(len(starting_cards))}_{time.time()}.json"
    return file_name