from training.src.game.classes import GameHistory, Player, State
from training.src.game.playing import play_trick
from training.src.learning.neural_nets import NeuralNetwork
from training.src.learning.replay_buffer import ReplayBuffer
from training.src.game.game_helpers import get_reward, get_actions, get_states
from training.src.agents.agent import register_agent, Agent

from typing import Callable, Type
from prettytable import PrettyTable
import numpy as np
import random
import torch

@register_agent
class DQNAgent(Agent):

    def __init__(self, k : int, hidden_sizes : tuple[int, int]):
        super().__init__(k)
        self.model = NeuralNetwork(input_shape=k*2, output_shape=k, hidden_sizes=hidden_sizes)
        self.hidden_sizes = hidden_sizes

    def play(self, game_history: GameHistory, args : dict):
        action = self.get_greedy_action(game_history)
        return action
    
    def _serialize(self, params : dict):
        # Convert tensor values to lists for JSON serialization
        state_dict = self.model.state_dict()
        serializable_state_dict = {k: v.tolist() for k, v in state_dict.items()}
        return {
                    "model_state_dict": serializable_state_dict,
                    "k": self.k,
                    "hidden_sizes": self.hidden_sizes,
                    "params": params
            }

    @classmethod
    def _deserialize(cls : Type["DQNAgent"], payload : dict) -> tuple["Agent", dict]:
        k = payload["k"]
        hidden_sizes = payload["hidden_sizes"]
        params = payload.get("params", {})
        agent = cls(k, hidden_sizes)
        state_dict = {k: torch.tensor(v) for k, v in payload["model_state_dict"].items()}
        agent.model.load_state_dict(state_dict)
        return agent, params

    def transform_state_to_input(self, state: State) -> torch.Tensor:
        player_0_cards, player_1_cards = state.get_cards(0), state.get_cards(1)
        p0_encoding = [1 if card in player_0_cards else 0 for card in range(self.k)]
        p1_encoding = [1 if card in player_1_cards else 0 for card in range(self.k)]
        input = p0_encoding + p1_encoding
        return torch.tensor(input, dtype=torch.float32).unsqueeze(0)

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.choice(get_actions(self.k, game_history.get_state()))
        return self.get_greedy_action(game_history)

    def get_greedy_action(self,  game_history: GameHistory) -> int:
        state = game_history.get_state()
        input = self.transform_state_to_input(state)
        q_values = self.model.apply(input)
        return self.get_best_action(state, q_values)[0]
    
    def get_best_action(self, state : State, q_values : np.ndarray) -> int:
        actions = get_actions(self.k, state)
        action_q_values = {a: q_values[a] for a in actions}
        max_q = max(action_q_values.values())
        max_actions = [a for a, q in action_q_values.items() if q == max_q]
        return random.choice(max_actions), max_q

    def train(
            self, 
            epochs: int, 
            epsilon : float, 
            learning_rate : float, 
            discount_factor : float, 
            replay_buffer_capacity : int,
            update_interval : int,
            minibatch_size : int,
            strategy : Callable[[Player, GameHistory], int]
    ):  
        
        game_history = GameHistory()
        replay_buffer = ReplayBuffer(capacity=replay_buffer_capacity)
        temp_model = NeuralNetwork(input_shape=self.k*2, output_shape=self.k, hidden_sizes=self.hidden_sizes)
        
        def agent_strategy(player: Player, game_history: GameHistory, args : dict) -> int:
            return self.play_eps_greedy(game_history, epsilon)
        
        player = Player(id=0, k=self.k, play_func=agent_strategy)
        opp_player = Player(id=1, k=self.k, play_func=strategy)

        round = 0
        for t in range(epochs):
            print(f"Epoch {t+1}/{epochs}", end="\r")
            
            # reset game if terminal state
            if game_history.get_state().is_terminal(self.k):
                game_history = GameHistory()
                player.reset()
                opp_player.reset()
                round += 1

            # play trick and add to replay buffer
            play_trick(player, opp_player, game_history, round)
            state, next_state = game_history.get_history()[-2], game_history.get_history()[-1]
            action = next_state.get_action(0)
            reward = get_reward(next_state)
            done = next_state.is_terminal(self.k)
            replay_buffer.push(state, action, reward, next_state, done)

            minibatch = replay_buffer.sample(minibatch_size)
            for state, action, reward, next_state, done in minibatch:

                # compute target
                target = reward
                if not done:
                    q_values_next = temp_model.apply(self.transform_state_to_input(next_state))
                    _, max_next_action_value = self.get_best_action(next_state, q_values_next)
                    target += discount_factor * max_next_action_value
                    
                # update target network
                input = self.transform_state_to_input(state)
                q_values = self.model.apply(input)
                q_values[action] = target
                target_tensor = torch.from_numpy(q_values).float().unsqueeze(0)
                self.model.train_step(input, target_tensor, learning_rate)

            # update behaviour network
            if t % update_interval == 0:
                temp_model.load_state_dict(self.model.state_dict())
    
    def print_q(self):
        table = PrettyTable()
        table.field_names = ["State", "Action", "Q-Value"]
        table.align["State"] = "l"
        table.align["Action"] = "c"  
        table.align["Q-Value"] = "r" 
        for state in get_states(self.k):
            q_values = self.model.apply(self.transform_state_to_input(state))
            actions = get_actions(self.k, state)
            for action in actions:
                q_value = q_values[self.get_action_index(action)]
                table.add_row([state, action, f"{q_value:.3f}"])
        print(table)