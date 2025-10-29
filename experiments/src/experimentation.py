from backend.src.options import list_card_counts, list_model_options, get_model_path
from training.src.util.seeding import set_global_seed
from training.src.agents.abstract.agent import Agent
from training.src.game.playing import play_rounds
from training.src.game.strategies import random_strategy, highest_strategy, copying_strategy, pool_strategy

# imports neccessary for agent registration
from training.src.agents.concrete.agent_DQN import DQNAgent
from training.src.agents.concrete.agent_STRAT import StrategyAgent
from training.src.agents.concrete.agent_PI import TabularAgent
from training.src.agents.concrete.agent_GRU import GRUAgent

import pandas as pd
import os

def get_seed(n1 : int, n2 : int) -> int:
    return 42 + n1 * 1000 + n2 * 4

def run_wl_experiments(n_evals : int, n_repeated_games : int) -> pd.DataFrame:

    data = []
    df = pd.DataFrame(columns=["model", "run", "seed", "adversarial_strategy", "k", "W", "T", "L", "games"])

    ks = list_card_counts()
    adversarial_strategies = [highest_strategy]

    for k in ks:
        for strategy in adversarial_strategies:
            adversarial_agent = StrategyAgent(k, strategy)
            adversarial_name = adversarial_agent.name().split("-")[1]
            for model_name in list_model_options(k, adversarial_name):
                model_path = get_model_path(k, adversarial_name, model_name)
                agent, _ = Agent.import_agent(model_path, k)
                for i in range(n_evals):
                    seed = get_seed(i, k)
                    set_global_seed(seed)
                    W, T, L = play_rounds(
                        n_rounds=n_repeated_games,
                        k=k,
                        agent_0=agent,
                        agent_1=adversarial_agent
                    )
                    row_data = {
                        "model": agent.name(),
                        "run": i,
                        "seed": seed,
                        "adversarial_strategy": adversarial_name,
                        "k": k,
                        "W": W / n_repeated_games,
                        "T": T / n_repeated_games,
                        "L": L / n_repeated_games,
                        "games": n_repeated_games
                    }
                    data.append(row_data)
    
    return pd.DataFrame(data)