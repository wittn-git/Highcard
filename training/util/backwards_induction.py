from util.classes import Card, GameHistory, Player, State
from util.helpers import get_states

from typing import Callable

def compare_strategies(
        starting_cards : list[Card],
        agent_strategy : Callable[[Player, GameHistory], Card],
        adversarial_strategy : Callable[[Player, GameHistory], Card]
) -> None:
    # This function should only be called with fixed-pool strategies for the adversarial strategy and with deterministic strategies for the agent strategy
    res = get_dict_from_strategy(starting_cards, adversarial_strategy)
    for k,v in res.items():
        print(k, ": ", v)
    pass # TODO finish implementation

def get_dict_from_strategy(
    starting_cards : list[Card],
    strategy : Callable[[Player, GameHistory], Card]
) -> dict[State, Card]:
    result_dict = {}
    game_history = GameHistory()
    for state in get_states(starting_cards):
        game_history.set_history(state)
        player_cards = [card for card in starting_cards if card not in state.get_cards(0)]
        player = Player(0, player_cards, strategy)
        action = strategy(player, game_history, {})
        result_dict[state] = action
    return result_dict

def backwards_induction(
    starting_cards : list[Card],
    adversarial_strategy : Callable[[Player, GameHistory], Card]
) -> dict[State, Card]:
    pass # TODO implement