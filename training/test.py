from training.agents.agent_PI import TabularAgent
from training.agents.agent_DQN import DQNAgent
from training.agents.agent_STRAT import StrategyAgent
from training.agents.agent import Agent
from training.util.playing import play_rounds
from training.util.strategies import random_strategy, highest_strategy, lowest_strategy
from training.util.seeding import seed
from training.util.backwards_induction import compare_strategies

import os

def get_test_filename():
    return "training/models/TEST.json"

def test_strategy_agent():
    k = 3
    adversarial_strategy = highest_strategy
    agent = StrategyAgent(k, random_strategy)
    strategy = agent.get_strategy()
    play_rounds(1, k, strategy, adversarial_strategy)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = StrategyAgent.import_agent(get_test_filename(), k)
    imported_strategy = imported_agent.get_strategy()
    play_rounds(1, k, imported_strategy, adversarial_strategy)

def test_tabular_agent():
    k = 3
    adversarial_strategy = highest_strategy
    agent = TabularAgent(k)
    agent.train(
        epochs=10,
        epsilon=0.1,
        learning_rate=0.1,
        discount_factor=1,
        strategy=adversarial_strategy
    )
    strategy = agent.get_strategy()
    play_rounds(1, k, strategy, adversarial_strategy)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = TabularAgent.import_agent(get_test_filename(), k)
    imported_strategy = imported_agent.get_strategy()
    play_rounds(1, k, imported_strategy, adversarial_strategy)

def test_dqn_agent():
    k = 3
    adversarial_strategy = highest_strategy
    agent = DQNAgent(k, hidden_sizes=(8,8))
    agent.train(
        epochs=10,
        epsilon=0.1,
        learning_rate=0.25,
        discount_factor=1,
        replay_buffer_capacity=64,
        update_interval=20,
        minibatch_size=32,
        strategy=adversarial_strategy
    )
    strategy = agent.get_strategy()
    play_rounds(1, k, strategy, adversarial_strategy)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = DQNAgent.import_agent(get_test_filename(), k)
    imported_strategy = imported_agent.get_strategy()
    play_rounds(1, k, imported_strategy, adversarial_strategy)

def test_comparison():
    k = 3
    agent, _ = Agent.import_agent(get_test_filename(), k)  
    strategy = agent.get_strategy()
    compare_strategies(k, strategy, [highest_strategy, lowest_strategy], False)

if __name__ == "__main__":

    seed(43)

    test_strategy_agent()
    test_tabular_agent()
    test_dqn_agent()

    test_comparison()

    if os.path.exists(get_test_filename()):
        os.remove(get_test_filename())