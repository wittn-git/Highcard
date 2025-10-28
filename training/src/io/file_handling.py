from training.src.game.classes import Player, StateHistory
from training.src.agents.abstract.agent import Agent

from typing import Callable
import time

def get_file_name(agent: Agent, k: int, adversarial_agent: Agent) -> str:
    return f"training/models/{agent.name()}_{adversarial_agent.name()}_{str(k)}_{str(time.time()).replace(".", "-")}.json"