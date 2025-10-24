from training.src.game.classes import Player, State
from training.src.agents.agent import Agent

from typing import Callable
import time

def get_file_name(agent: Agent, k: int, adversarial_strategy: Callable[[Player, State], int]) -> str:
    strategy_string = ""
    if adversarial_strategy != None:
        strategy_name = adversarial_strategy.__name__.replace("_", "-")
        strategy_string = "_" + strategy_name.lower()
    agent_type = type(agent).__name__.replace("Agent", "")
    file_name = f"training/models/{agent_type.lower()}{strategy_string}_{str(k)}_{str(time.time()).replace(".", "-")}.json"
    return file_name