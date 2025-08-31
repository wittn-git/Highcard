from util.util import play_rounds, play_round
from util.strategies import random_strategy, highest_card_strategy
from util.classes import Card
from agents.agent_PI import TabularAgent

import random

if __name__ == "__main__":

    starting_cards = [Card(i) for i in range(0, 5)]
    n_rounds = 10000
    adversarial_strategy = highest_card_strategy

    random.seed(42)
    agent = TabularAgent(starting_cards)
    agent.train(epochs=10000, epsilon=0.1, learning_rate=0.1, discount_factor=0.9, strategy=adversarial_strategy)
    strategy = agent.get_strategy()
    
    results = play_rounds(n_rounds, starting_cards, strategy, adversarial_strategy)
    play_round(starting_cards, strategy, adversarial_strategy, True)

    print("-----------------------")
    print("Results after", n_rounds, "rounds:")
    print("Player 1 wins:", results[0])
    print("Player 2 wins:", results[1])
    print("Draws:", results[2])