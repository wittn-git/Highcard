from training.util.classes import Player, GameHistory
from training.agents.agent_PI import TabularAgent
from training.agents.agent_DQN import DQNAgent
from training.agents.agent_STRAT import StrategyAgent
from training.agents.agent import Agent
from training.util.playing import play_rounds
from training.util.strategies import random_strategy, highest_strategy, lowest_strategy, fixed_pool_strategy
from training.util.file_handling import get_file_name
from training.util.seeding import seed
from training.util.backwards_induction import compare_strategies

from typing import Callable

def train_tabular_agent(
        k : int, 
        adversarial_strategy : Callable[[Player, GameHistory], int],
        params : dict
) -> Agent:
    agent = TabularAgent(k)
    agent.train(
       epochs=params["epochs"],
       epsilon=params["epsilon"],
       learning_rate=params["learning_rate"], 
       discount_factor=params["discount_factor"], 
       strategy=adversarial_strategy
    )
    agent.export_agent(get_file_name(agent, k, adversarial_strategy), params)
    return agent

def train_dqn_agent(
        k : int, 
        adversarial_strategy : Callable[[Player, GameHistory], int],
        params : dict
) -> Agent:
    agent = DQNAgent(k, hidden_sizes=params["hidden_sizes"])
    agent.train(
        epochs=params["epochs"], 
        epsilon=params["epsilon"], 
        learning_rate=params["learning_rate"], 
        discount_factor=params["discount_factor"], 
        replay_buffer_capacity=params["replay_buffer_capacity"],
        update_interval=params["update_interval"],
        minibatch_size=params["minibatch_size"],
        strategy=adversarial_strategy
    )
    agent.export_agent(get_file_name(agent, k, adversarial_strategy), params)
    return agent

def train_strategy_agent(
        k : int, 
        strategy : Callable[[Player, GameHistory], int]
) -> Agent:
    agent = StrategyAgent(k, strategy)
    agent.export_agent(get_file_name(agent, k, strategy), {})
    return agent

def test_agent(
        k : int,
        file_name: str, 
        evaluation_rounds: int, 
        adversarial_strategy : Callable[[Player, GameHistory], int]
) -> Agent:
    agent, _ = Agent.import_agent(file_name, k)  
    strategy = agent.get_strategy()
    results = play_rounds(evaluation_rounds, k, strategy, adversarial_strategy)
    print("-------------------------------")
    print("Results after", evaluation_rounds, "rounds:")
    print("Player 1 wins:", results[0])
    print("Player 2 wins:", results[1])
    print("Draws:", results[2])
    return agent

def compare_agent(
        k : int,
        file_name: str, 
        adversarial_strategies : list[Callable[[Player, GameHistory], int]]
):
    agent, _ = Agent.import_agent(file_name, k)  
    strategy = agent.get_strategy()
    compare_strategies(k, strategy, adversarial_strategies)

if __name__ == "__main__":

    seed(43)
    k = 5
    adversarial_strategy = highest_strategy
    file_name = "/home/wittn/workspace/Highcard/training/models/tabular_highest-strategy_5.json"
    
    # params_tabular = {
    #     "epochs": 5000,
    #     "learning_rate": 0.1,
    #     "discount_factor": 1,
    #     "epsilon": 0.1
    # }
    # train_tabular_agent(k, adversarial_strategy, params_tabular)

    # params_dqn = {
    #     "epochs": 5000,
    #     "learning_rate": 0.25,
    #     "discount_factor": 1,
    #     "epsilon": 0.1,
    #     "replay_buffer_capacity": 64,
    #     "update_interval": 20,
    #     "minibatch_size": 32,
    #     "hidden_sizes": (8, 8)
    # }
    # train_dqn_agent(k, adversarial_strategy, params_dqn)

    # train_strategy_agent(k, adversarial_strategy)

    # test_agent(k, file_name, 100, adversarial_strategy)
    # compare_agent(k, file_name, [adversarial_strategy])