from util.classes import Card, GameHistory, Player, State
from util.playing import play_trick
from util.neural_nets import NeuralNetwork
from util.replay_buffer import ReplayBuffer
from util.helpers import is_terminal, get_reward, get_actions, get_states
from agents.agent import register_agent, Agent

from typing import List, Callable, Type
from prettytable import PrettyTable
import random
import torch

@register_agent
class DQNAgent(Agent):

    def __init__(self, starting_cards : List[Card]):
        super().__init__(starting_cards)
        self.model = NeuralNetwork(input_shape=len(starting_cards)*3, output_shape=1)

    def play(self, game_history: GameHistory):
        action = self.get_greedy_action(game_history)
        return action
    
    def _serialize(self):
        return {
                    "model_state_dict": self.model.state_dict(),
                    "starting_cards": [c.value for c in self.starting_cards]
            }

    @classmethod
    def _deserialize(cls : Type["DQNAgent"], payload : dict):
        starting_cards = [Card(c) for c in payload["starting_cards"]]
        agent = cls(starting_cards)
        agent.model.load_state_dict(payload["model_state_dict"])
        return agent

    def transform_state_to_input(self, state: State, action : Card) -> torch.Tensor:
        player_0_cards, player_1_cards = state.get_cards(0), state.get_cards(1)
        p0_encoding = [1 if card in player_0_cards else 0 for card in self.starting_cards]
        p1_encoding = [1 if card in player_1_cards else 0 for card in self.starting_cards]
        action_encoding = [1 if card == action else 0 for card in self.starting_cards]
        input = p0_encoding + p1_encoding + action_encoding
        return torch.tensor(input, dtype=torch.float32).unsqueeze(0)

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> Card:
        if random.random() < epsilon:
            return random.choice(get_actions(self.starting_cards, game_history.get_state()))
        return self.get_greedy_action(game_history)

    def get_greedy_action(self,  game_history: GameHistory) -> Card:
        state = game_history.get_state()
        actions = get_actions(self.starting_cards, state)
        if len(actions) == 1:
            return actions[0]
        best_value = float('-inf')
        best_action = actions[0]
        for action in actions:
            input = self.transform_state_to_input(state, action)
            output = self.model.forward(input)
            q_value = output.item()
            if q_value > best_value:
                best_value = q_value
                best_action = action
        return best_action

    def train(
            self, 
            epochs: int, 
            epsilon : float, 
            learning_rate : float, 
            discount_factor : float, 
            replay_buffer_capacity : int,
            update_interval : int,
            minibatch_size : int,
            strategy : Callable[[Player, GameHistory], Card]
    ):  
        
        game_history = GameHistory()
        replay_buffer = ReplayBuffer(capacity=replay_buffer_capacity)
        temp_model = NeuralNetwork(input_shape=len(self.starting_cards)*3, output_shape=1)
        
        def agent_strategy(player: Player, game_history: GameHistory) -> Card:
            return self.play_eps_greedy(game_history, epsilon)
        
        player = Player(id=0, starting_cards=self.starting_cards, play_func=agent_strategy)
        opp_player = Player(id=1, starting_cards=self.starting_cards, play_func=strategy)

        for t in range(epochs):
            print(f"Epoch {t+1}/{epochs}", end="\r")
            
            # reset game if terminal state
            if is_terminal(self.starting_cards, game_history.get_state()):
                game_history = GameHistory()
                player.reset()
                opp_player.reset()

            # play trick and add to replay buffer
            play_trick(player, opp_player, game_history)
            state, next_state = game_history.get_history()[-2], game_history.get_history()[-1]
            action = next_state.get_action(0)
            reward = get_reward(next_state)
            done = is_terminal(self.starting_cards, next_state)
            replay_buffer.push(state, action, reward, next_state, done)

            minibatch = replay_buffer.sample(minibatch_size)
            for state, action, reward, next_state, done in minibatch:

                # compute target
                target = reward
                if not done:
                    max_next_action_value = 0
                    for action in get_actions(self.starting_cards, next_state):
                        next_state_input = self.transform_state_to_input(next_state, action)
                        next_action_value = temp_model.forward(next_state_input).item()
                        if next_action_value > max_next_action_value:
                            max_next_action_value = next_action_value
                    target += discount_factor * max_next_action_value

                # update target network
                input = self.transform_state_to_input(state, action)
                target_tensor = torch.tensor([[target]], dtype=torch.float32)  # Shape [1, 1] to match network output
                self.model.train_step(input, target_tensor, learning_rate)

            # update behaviour network
            if t % update_interval == 0:
                temp_model.load_state_dict(self.model.state_dict())
    
    def print_q(self):
        table = PrettyTable()
        table.field_names = ["State", "Action", "Q-Value"]
        table.align = "l"
        for state in get_states(self.starting_cards):
            for action in get_actions(self.starting_cards, state):
                input = self.transform_state_to_input(state, action)
                q_value = self.model.forward(input).item()
                table.add_row([state, action, q_value])
        print(table)