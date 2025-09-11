from util.classes import Card
from agents.agent_PI import TabularAgent
from agents.agent_DQN import DQNAgent
from util.playing import play_rounds, play_round
from util.strategies import random_strategy, highest_card_strategy

import random
import numpy as np
import torch

def seed(seed_value: int):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)

if __name__ == "__main__":

    seed(43)

    starting_cards = [Card(i) for i in range(0, 4)]
    n_rounds = 100
    adversarial_strategy = highest_card_strategy
    epochs, learning_rate, discount_factor = 5000, 0.1, 1

    ## Training Tabular Agent
    """ agent = TabularAgent(starting_cards)
    agent.train(
       epochs=epochs,
       epsilon=0.1,
       learning_rate=learning_rate,
       discount_factor=discount_factor,
       strategy=adversarial_strategy
    )
    agent.export_agent("models/tabular_agent.json") """

    # Import Tabular Agent
    # agent = TabularAgent.import_agent("models/tabular_agent.json")

    # Training DQN Agent
    agent = DQNAgent(starting_cards, hidden_sizes=(16, 16))
    agent.train(
       epochs=epochs, 
       epsilon=0.1, 
       learning_rate=learning_rate, 
       discount_factor=discount_factor, 
       replay_buffer_capacity=64,
       update_interval=20,
       minibatch_size=32,
       strategy=adversarial_strategy
    )
    agent.print_q()
    agent.export_agent("models/dqn_agent.json")

    # Import DQN Agent
    # agent = DQNAgent.import_agent("models/dqn_agent.json")

    strategy = agent.get_strategy()
    results = play_rounds(n_rounds, starting_cards, strategy, adversarial_strategy)
    play_round(starting_cards, strategy, adversarial_strategy, True)

    print("-------------------------------")
    print("Results after", n_rounds, "rounds:")
    print("Player 1 wins:", results[0])
    print("Player 2 wins:", results[1])
    print("Draws:", results[2])