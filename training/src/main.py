from training.src.game.classes import Player, StateHistory
from training.src.agents.concrete.agent_PI import TabularAgent
from training.src.agents.concrete.agent_DQN import DQNAgent
from training.src.agents.concrete.agent_STRAT import StrategyAgent
from training.src.agents.abstract.agent import Agent
from training.src.game.playing import play_rounds
from training.src.game.strategies import random_strategy, highest_strategy, lowest_strategy
from training.src.io.file_handling import get_file_name
from training.src.util.seeding import seed
from training.src.other.backwards_induction import compare_strategies

from typing import Callable

def train_tabular_agent(
        k: int, 
        adversarial_agent: Agent,
        params: dict
) -> Agent:
    agent = TabularAgent(k)
    agent.train(
       epochs=params["epochs"],
       epsilon=params["epsilon"],
       learning_rate=params["learning_rate"], 
       discount_factor=params["discount_factor"], 
       adversarial_agent=adversarial_agent
    )
    agent.export_agent(get_file_name(agent, k, adversarial_agent), params)
    return agent

def train_dqn_agent(
        k: int, 
        adversarial_agent: Agent,
        params: dict
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
        adversarial_agent=adversarial_agent
    )
    agent.export_agent(get_file_name(agent, k, adversarial_agent), params)
    return agent

def train_strategy_agent(
        k: int, 
        strategy: Callable[[Player, StateHistory], int]
) -> Agent:
    agent = StrategyAgent(k, strategy)
    agent.export_agent(get_file_name(agent, k, strategy), {})
    return agent

def test_agent(
        k: int,
        file_name: str, 
        evaluation_rounds: int, 
        adversarial_agent: Agent,
) -> Agent:
    agent, _ = Agent.import_agent(file_name, k)
    results = play_rounds(evaluation_rounds, k, agent, adversarial_agent)
    print("-------------------------------")
    print("Results after", evaluation_rounds, "rounds:")
    print("Player 1 wins:", results[0])
    print("Player 2 wins:", results[1])
    print("Draws:", results[2])
    return agent

def compare_agent(
        k: int,
        file_name: str, 
        adversarial_strategies : list[Callable[[Player, StateHistory], int]],
):
    agent, _ = Agent.import_agent(file_name, k)  
    compare_strategies(k, agent, adversarial_strategies)

if __name__ == "__main__":

    seed(43)
    k = 5
    adversarial_strategy = highest_strategy
    
    params_tabular = {
        "epochs": 5000,
        "learning_rate": 0.1,
        "discount_factor": 1,
        "epsilon": 0.1
    }
    train_tabular_agent(k, StrategyAgent(k, adversarial_strategy), params_tabular)
    
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
    # train_dqn_agent(k, StrategyAgent(k, adversarial_strategy), params_dqn)

    # train_strategy_agent(k, adversarial_strategy)

    # test_agent(k, file_name, 100, StrategyAgent(k, adversarial_strategy))

    # file_name = "/home/wittn/workspace/Highcard/training/models/tabular_highest-strategy_5.json"
    # compare_agent(k, file_name, agent, [adversarial_strategy])