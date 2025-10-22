from training.util.classes import Card
from training.agents.agent_PI import TabularAgent
from training.agents.agent_DQN import DQNAgent
from training.agents.agent import Agent
from training.util.playing import play_rounds, play_round
from training.util.strategies import random_strategy, highest_strategy, lowest_strategy, fixed_pool_strategy
from training.util.file_handling import get_file_name
from training.util.seeding import seed
from training.util.backwards_induction import compare_strategies

def get_agent(starting_cards : list[Card]) -> Agent:
    ## Training Tabular Agent
    # params_tabular = {
    #     "epochs": 5000,
    #     "learning_rate": 0.1,
    #     "discount_factor": 1,
    #     "epsilon": 0.1
    # }
    # agent = TabularAgent(starting_cards)
    # agent.train(
    #    epochs=params_tabular["epochs"],
    #    epsilon=params_tabular["epsilon"],
    #    learning_rate=params_tabular["learning_rate"], 
    #    discount_factor=params_tabular["discount_factor"], 
    #    strategy=adversarial_strategy
    # )
    # agent.export_agent(get_file_name(agent, adversarial_strategy, starting_cards), params_tabular)

    # Import Tabular Agent
    agent, _ = TabularAgent.import_agent("models/tabularagent_fixed-pool-strategy_3_1760956078.0740678.json", starting_cards)
    # agent.print_q()

    # Training DQN Agent
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
    # agent = DQNAgent(starting_cards, hidden_sizes=params_dqn["hidden_sizes"])
    # agent.train(
    #     epochs=params_dqn["epochs"], 
    #     epsilon=params_dqn["epsilon"], 
    #     learning_rate=params_dqn["learning_rate"], 
    #     discount_factor=params_dqn["discount_factor"], 
    #     replay_buffer_capacity=params_dqn["replay_buffer_capacity"],
    #     update_interval=params_dqn["update_interval"],
    #     minibatch_size=params_dqn["minibatch_size"],
    #     strategy=adversarial_strategy
    # )
    # agent.print_q()
    # agent.export_agent(get_file_name(agent, adversarial_strategy, starting_cards), params_dqn)

    # Import DQN Agent
    # agent, _ = DQNAgent.import_agent("models/XXX", starting_cards)

    return agent

def run_single_evaluation():

    seed(43)

    starting_cards = [Card(i) for i in range(0, 3)]
    evaluation_rounds = 100
    adversarial_strategy = fixed_pool_strategy
    
    agent = get_agent(starting_cards)
    strategy = agent.get_strategy()

    results = play_rounds(evaluation_rounds, starting_cards, strategy, adversarial_strategy)
    play_round(starting_cards, strategy, adversarial_strategy, True)

    print("-------------------------------")
    print("Results after", evaluation_rounds, "rounds:")
    print("Player 1 wins:", results[0])
    print("Player 2 wins:", results[1])
    print("Draws:", results[2])

def compare_agent():
    
    seed(43)

    starting_cards = [Card(i) for i in range(0, 3)]
    adversarial_strategies = [highest_strategy]
    agent = get_agent(starting_cards)
    strategy = agent.get_strategy()

    compare_strategies(starting_cards, strategy, adversarial_strategies)

if __name__ == "__main__":
    pass
    # run_single_evaluation()
    # compare_agent()