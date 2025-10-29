from training.src.agents.abstract.agent import Agent

import time

def get_file_name(agent: Agent, k: int, adversarial_agent: Agent) -> str:
    adversarial_name = adversarial_agent.name()
    if adversarial_name.startswith("strat-"):
        adversarial_name = adversarial_name.split("-")[1]
    return f"training/models/{agent.name()}_{adversarial_name}_{str(k)}_{str(time.time()).replace(".", "-")}.json"