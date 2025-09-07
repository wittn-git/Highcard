from util.classes import Card, GameHistory, Player, State
from agents.agent import Agent, register_agent
from util.playing import play_round
from util.helpers import is_terminal, get_reward, get_actions, get_states

from typing import List, Callable, Type
from prettytable import PrettyTable
import random
import ast

@register_agent
class TabularAgent(Agent):

    def __init__(self, starting_cards : List[Card]):
        super().__init__(starting_cards)
        states = get_states(starting_cards)
        self.q = {(s, a): 0 for s in states for a in get_actions(starting_cards, s)}
    
    def play(self, game_history: GameHistory):
        action = self.get_greedy_action(game_history)
        return action
    
    def _serialize(self):
        return {
                    "q": {
                        str(([card.value for card in state.get_cards(0)] + [card.value for card in state.get_cards(1)], action.value)): value
                        for (state, action), value in self.q.items()
                    },
                    "starting_cards": [c.value for c in self.starting_cards]
            }

    @classmethod
    def _deserialize(cls : Type["TabularAgent"], payload : dict):
        starting_cards = [Card(c) for c in payload["starting_cards"]]
        agent = cls(starting_cards)
        agent.q = {}
        for key, value in payload["q"].items():
            card_values, action_value = ast.literal_eval(key)
            p0_cards, p1_cards = tuple(Card(c) for c in card_values[:len(card_values)//2]), tuple(Card(c) for c in card_values[len(card_values)//2:])
            state = State(p0_cards, p1_cards)
            action = Card(action_value)
            agent.q[(state, action)] = value
        return agent

    def play_eps_greedy(self, game_history: GameHistory, epsilon: float) -> Card:
        if random.random() < epsilon:
            return random.choice(get_actions(self.starting_cards, game_history.get_state()))
        return self.get_greedy_action(game_history)

    def train(
            self, 
            epochs: int, 
            epsilon : float, 
            learning_rate : float, 
            discount_factor : float, 
            strategy : Callable[[Player, GameHistory], Card]
    ):
        for _ in range(epochs):
            def agent_strategy(player: Player, game_history: GameHistory) -> Card:
                return self.play_eps_greedy(game_history, epsilon)
            game_history = play_round(self.starting_cards, agent_strategy, strategy)
            trajectory = game_history.get_history()
            for i in range(len(trajectory)-1):
                state, next_state = trajectory[i], trajectory[i+1]
                action = next_state.get_action(0)
                next_state_value = 0
                if not is_terminal(self.starting_cards, next_state):
                    next_action = self.get_greedy_action(next_state)
                    next_state_value = self.q[(next_state, next_action)]
                reward = get_reward(next_state)
                self.q[(state, action)] += learning_rate * (reward + discount_factor * next_state_value - self.q[(state, action)])

    def get_greedy_action(self, game_history: GameHistory):
        state = game_history.get_state()
        actions = get_actions(self.starting_cards, state)
        q_values = [self.q[(state, a)] for a in actions]
        max_q = max(q_values)
        max_actions = [a for (a, q) in zip(actions, q_values) if q == max_q]
        return random.choice(max_actions)
    
    def print_q(self):
        table = PrettyTable()
        table.field_names = ["State", "Action", "Q-Value"]
        table.align = "l"
        for ((s, a), val) in self.q.items():
            table.add_row([s, a, val])
        print(table)