from backend.src.options import list_card_counts, list_model_options, list_adversarial_options, get_model_path
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

    ks = list_card_counts()
    test_adversarial_strategies = [highest_strategy]

    for k in ks:
        for strategy in test_adversarial_strategies:
            test_adversarial_agent = StrategyAgent(k, strategy)
            test_adversarial_name = test_adversarial_agent.name().split("-")[1]
            for train_adversarial_strategy in list_adversarial_options(k):
                for model_name in list_model_options(k, train_adversarial_strategy):
                    model_path = get_model_path(k, train_adversarial_strategy, model_name)
                    agent, _ = Agent.import_agent(model_path, k)
                    for i in range(n_evals):
                        seed = get_seed(i, k)
                        set_global_seed(seed)
                        W, L, T = play_rounds(
                            n_rounds=n_repeated_games,
                            k=k,
                            agent_0=agent,
                            agent_1=test_adversarial_agent
                        )
                        row_data = {
                            "model": model_name,
                            "run": i,
                            "seed": seed,
                            "adversarial_strategy_train": train_adversarial_strategy,
                            "adversarial_strategy_test": test_adversarial_name,
                            "k": k,
                            "win_rate": W / n_repeated_games,
                            "tie_rate": T / n_repeated_games,
                            "loss_rate": L / n_repeated_games,
                            "games": n_repeated_games
                        }
                        data.append(row_data)
    
    return pd.DataFrame(data)