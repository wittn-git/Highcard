from util.classes import Card
from agents.agent_PI import TabularAgent
from util.playing import play_rounds, play_round
from util.strategies import random_strategy, highest_card_strategy

import random

if __name__ == "__main__":

    starting_cards = [Card(i) for i in range(0, 5)]
    n_rounds = 100
    adversarial_strategy = highest_card_strategy
    epochs, learning_rate, discount_factor = 10000, 0.1, 0.9

    random.seed(42)
    agent = TabularAgent(starting_cards)
    agent.train(epochs=epochs, epsilon=0.1, learning_rate=learning_rate, discount_factor=discount_factor, strategy=adversarial_strategy)
    strategy = agent.get_strategy()
    
    results = play_rounds(n_rounds, starting_cards, strategy, adversarial_strategy)
    play_round(starting_cards, strategy, adversarial_strategy, True)

    print("-------------------------------")
    print("Results after", n_rounds, "rounds:")
    print("Player 1 wins:", results[0])
    print("Player 2 wins:", results[1])
    print("Draws:", results[2])