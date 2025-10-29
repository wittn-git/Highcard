from training.src.agents.concrete.agent_PI import TabularAgent
from training.src.agents.concrete.agent_DQN import DQNAgent
from training.src.agents.concrete.agent_STRAT import StrategyAgent
from training.src.agents.concrete.agent_GRU import GRUAgent
from training.src.agents.abstract.agent import Agent
from training.src.game.playing import play_rounds
from training.src.game.strategies import random_strategy, highest_strategy, lowest_strategy
from training.src.util.seeding import seed_rnd
from training.src.other.backwards_induction import compare_strategies

import os

def get_test_filename():
    return "training/models/TEST.json"

def test_strategy_agent():
    k = 3
    agent = StrategyAgent(k, random_strategy)
    adversarial_agent = StrategyAgent(k, highest_strategy)
    play_rounds(1, k, agent, adversarial_agent)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = StrategyAgent.import_agent(get_test_filename(), k)
    play_rounds(1, k, imported_agent, adversarial_agent)

def test_tabular_agent():
    k = 3
    adversarial_agent = StrategyAgent(k, highest_strategy)
    agent = TabularAgent(k)
    agent.train(
        epochs=10,
        epsilon=0.1,
        learning_rate=0.1,
        discount_factor=1,
        seed=42,
        adversarial_agent=adversarial_agent
    )
    play_rounds(1, k, agent, adversarial_agent)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = TabularAgent.import_agent(get_test_filename(), k)
    play_rounds(1, k, imported_agent, adversarial_agent)

def test_dqn_agent():
    k = 3
    adversarial_agent = StrategyAgent(k, highest_strategy)
    agent = DQNAgent(k, hidden_sizes=(8,8))
    agent.train(
        epochs=10,
        epsilon=0.1,
        learning_rate=0.25,
        discount_factor=1,
        replay_buffer_capacity=64,
        update_interval=20,
        minibatch_size=32,
        seed=42,
        adversarial_agent=adversarial_agent
    )
    play_rounds(1, k, agent, adversarial_agent)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = DQNAgent.import_agent(get_test_filename(), k)
    play_rounds(1, k, imported_agent, adversarial_agent)

def test_gru_agent():
    k = 3
    adversarial_agent = StrategyAgent(k, highest_strategy)
    agent = GRUAgent(k, layer_n=1, hidden_size=8)
    agent.train(
        epochs=10,
        epsilon=0.1,
        learning_rate=0.25,
        discount_factor=1,
        replay_buffer_capacity=64,
        update_interval=20,
        minibatch_size=32,
        seed=42,
        adversarial_agent=adversarial_agent
    )
    play_rounds(1, k, agent, adversarial_agent)
    agent.export_agent(get_test_filename(), {})
    imported_agent, _ = GRUAgent.import_agent(get_test_filename(), k)
    play_rounds(1, k, imported_agent, adversarial_agent)

def test_comparison():
    k = 3
    agent, _ = Agent.import_agent(get_test_filename(), k)  
    compare_strategies(k, agent, [highest_strategy, lowest_strategy], False)

if __name__ == "__main__":

    test_strategy_agent()
    test_tabular_agent()
    test_dqn_agent()
    test_gru_agent()

    test_comparison()

    if os.path.exists(get_test_filename()):
        os.remove(get_test_filename())