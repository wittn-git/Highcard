from training.src.game.classes import Player, State, StateHistory
from training.src.game.playing import play_trick
from training.src.learning.gru_net import GRUNet
from training.src.other.replay_buffer import ReplayBuffer
from training.src.game.game_helpers import get_reward, get_actions
from training.src.agents.abstract.agent import register_agent, Agent
from training.src.agents.abstract.agent_deep import DeepAgent
from training.src.agents.concrete.agent_STRAT import StrategyAgent
from training.src.util.seeding import seed_rnd

from typing import Type
import random
import torch

@register_agent
class GRUAgent(DeepAgent):

    def __init__(self, k: int, layer_n: int, hidden_size: int):
        super().__init__(k)
        self.model = GRUNet(input_shape=k*2, output_shape=k, layer_n=layer_n, hidden_size=hidden_size)
        self.layer_n, self.hidden_size = layer_n, hidden_size
        self.hidden_state = None
    
    # Serialization methods

    def _serialize(self, params: dict) -> dict:
        # Convert tensor values to lists for JSON serialization
        state_dict = self.model.state_dict()
        serializable_state_dict = {k: v.tolist() for k, v in state_dict.items()}
        return {
                    "model_state_dict": serializable_state_dict,
                    "k": self.k,
                    "hidden_size": self.hidden_size,
                    "layer_n": self.layer_n,
                    "params": params
            }

    @classmethod
    def _deserialize(cls: Type["GRUAgent"], payload: dict) -> tuple["Agent", dict]:
        k = payload["k"]
        layer_n = payload["layer_n"]
        hidden_size = payload["hidden_size"]
        params = payload.get("params", {})
        agent = cls(k, layer_n, hidden_size)
        state_dict = {k: torch.tensor(v) for k, v in payload["model_state_dict"].items()}
        agent.model.load_state_dict(state_dict)
        return agent, params
    
    # Playing methods

    def play(self, cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
        state = state_history.top(player_id)
        return self.get_greedy_action(state)
    
    def play_eps_greedy(self, state: State, epsilon: float) -> int:
        if random.random() < epsilon:
            return random.choice(get_actions(self.k, state))
        return self.get_greedy_action(state)

    def get_greedy_action(self, state: State) -> int:
        input = self.transform_state_to_input(state)
        q_values, self.hidden_state = self.model.apply(input, self.hidden_state)
        return self.get_best_action(state, q_values)[0]
    
    # Training method
    
    def train(
        self, 
        epochs: int, 
        epsilon: float, 
        learning_rate: float, 
        discount_factor: float, 
        replay_buffer_capacity: int,
        update_interval: int,
        minibatch_size: int,
        seed: int,
        adversarial_agent: Agent,
    ):
        
        seed_rnd(seed)
        
        replay_buffer = ReplayBuffer(capacity=replay_buffer_capacity)
        temp_model = GRUNet(input_shape=self.k * 2, output_shape=self.k, layer_n=self.layer_n, hidden_size=self.hidden_size)
        temp_hidden_state = None

        def agent_strategy(cards: list[int], state_history: StateHistory, player_id: int, args: dict) -> int:
            return self.play_eps_greedy(state_history.top(), epsilon)
        
        player = Player(id=0, k=self.k, agent=StrategyAgent(self.k, agent_strategy))
        opp_player = Player(id=1, k=self.k, agent=adversarial_agent)

        state_history= StateHistory(self.k)
        round = 0

        for t in range(epochs):
            print(f"Epoch {t+1}/{epochs}", end="\r")

            # reset game if terminal state
            if state_history.is_terminal():
                state_history.push(State(self.k))
                player.reset()
                opp_player.reset()
                round += 1

            # play trick (returns the next state)
            state_history = play_trick(player, opp_player, state_history)

            # extract transition
            next_state = state_history.top()
            state = next_state.get_predecessor()
            action = next_state.get_action(0)
            reward = get_reward(next_state)
            done = next_state.is_terminal()

            # add transition to replay buffer
            replay_buffer.push(state.copy(), action, reward, next_state.copy(), done)

            # training step
            minibatch = replay_buffer.sample(minibatch_size)
            for state_, action_, reward_, next_state_, done_ in minibatch:
                
                # compute target
                target = reward_
                if not done_:
                    q_values_next, temp_hidden_state = temp_model.apply(self.transform_state_to_input(next_state_), temp_hidden_state)
                    _, max_next_action_value = self.get_best_action(next_state_, q_values_next)
                    target += discount_factor * max_next_action_value
                    
                # update model
                input = self.transform_state_to_input(state_)
                q_values, self.hidden_state = self.model.apply(input, self.hidden_state)
                q_values[action_] = target
                target_tensor = torch.from_numpy(q_values).float().unsqueeze(0)
                self.model.train_step(input, target_tensor, learning_rate)

            # update behaviour network
            if t % update_interval == 0:
                temp_model.load_state_dict(self.model.state_dict())
    
    def name(self):
        return "gru"