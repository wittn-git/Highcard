from training.util.classes import GameHistory, Player, State
from training.util.helpers import get_states

import math

from typing import Callable

def compare_strategies(
        k : int,
        agent_strategy : Callable[[Player, GameHistory], int],
        adversarial_strategies : list[Callable[[Player, GameHistory], int]],
        verbose : bool = True
) -> None:
    # This function should only be called with a pool of deterministic strategies for the adversarial strategies and with deterministic strategies for the agent strategy
    
    agent_reactions = get_dict_from_strategy(k, agent_strategy, State((), ()))
    optimal_reactions = backwards_induction(k, adversarial_strategies)

    optimal_actions, suboptimal_actions = 0, 0
    for k, v in optimal_reactions.items():
        if k not in agent_reactions:
            continue
        if agent_reactions[k] in v:
            optimal_actions += 1
        else:
            suboptimal_actions += 1
    if verbose:
        print(f"Optimal actions taken: {optimal_actions}")
        print(f"Suboptimal actions taken: {suboptimal_actions}")

def get_dict_from_strategy(k : int, strategy : Callable[[Player, GameHistory], int], state : State, action_dict : dict[State, int] = {}) -> dict[State, int]:
    if state.is_terminal(k):
        return action_dict
    player_cards = state.get_residual_cards(1, k)
    action = strategy(Player(1, k, strategy, player_cards), GameHistory(state), {})
    action_dict[state] = action
    ad_player_cards = state.get_residual_cards(1, k)
    for ad_card in ad_player_cards:
        successor_state = State.get_successor(state, action, ad_card)
        action_dict = get_dict_from_strategy(k, strategy, successor_state, action_dict)
    return action_dict

class Node:

    def __init__(self, state : State, k : int, probability : float, strategies :  list[Callable[[Player, GameHistory], int]]):
        
        self.state = state
        self.k = k

        if self.state.is_terminal(self.k):
            self.value = self.state.get_game_scores()[0] * probability
        else:
            self.children = self.get_children(strategies)
            children_values = {card: sum([child.value for child in card_children]) for card, card_children in self.children.items()}
            max_val = max(children_values.values())
            self.optimal_actions = [card for card, val in children_values.items() if val == max_val]
            self.value = max_val * probability
    
    def get_adversarial_probabilities(self, strategies :  list[Callable[[Player, GameHistory], int]]) -> dict[int, float]:
        ad_player_cards = self.state.get_residual_cards(1, self.k)
        ad_played_cards = {card: 0 for card in ad_player_cards}
        game_history = GameHistory(self.state)
        for strategy in strategies:
            ad_player = Player(1, self.k, strategy, ad_player_cards)
            adversarial_card = strategy(ad_player, game_history, {})
            ad_played_cards[adversarial_card] += 1
        ad_player_probs = {card: x / len(strategies) for (card, x) in ad_played_cards.items() if x > 0}
        return ad_player_probs

    def get_children(self, strategies :  list[Callable[[Player, GameHistory], int]]) -> dict[int, list["Node"]]:
        player_cards = self.state.get_residual_cards(0, self.k)
        ad_player_probs = self.get_adversarial_probabilities(strategies)
        children = {}
        for card in player_cards:
            card_children = []
            for ad_card in ad_player_probs.keys():
                card_children.append(Node(State.get_successor(self.state, card, ad_card), self.k, ad_player_probs[ad_card], strategies))
            children[card] = card_children
        return children

    def get_optimal_action_dict(self, optimal_action_dict : dict[State, list[int]] = {}):
        if self.state.is_terminal(self.k):
            return optimal_action_dict
        optimal_action_dict[self.state] = self.optimal_actions
        for card_children in self.children.values():
            for child in card_children:
                optimal_action_dict = child.get_optimal_action_dict(optimal_action_dict)
        return optimal_action_dict

def backwards_induction(k : int, adversarial_strategies :  list[Callable[[Player, GameHistory], int]]) -> dict[State, int]:
    game_tree = Node(State((), ()), k, 1.0, adversarial_strategies)
    return game_tree.get_optimal_action_dict()