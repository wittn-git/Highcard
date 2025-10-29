from training.src.agents.abstract.agent import Agent
from training.src.game.classes import Player, State, StateHistory
from backend.src.options import get_model_path

# imports neccessary for agent registration
from training.src.agents.concrete.agent_DQN import DQNAgent
from training.src.agents.concrete.agent_STRAT import StrategyAgent
from training.src.agents.concrete.agent_PI import TabularAgent
from training.src.agents.concrete.agent_GRU import GRUAgent

from typing import Callable

_loaded_agent, _state_history = None, None

def load_model(model_name: str, k: int, adversarial: str) -> Callable[[Player, StateHistory], int]:
    global _loaded_agent, _state_history
    model_path = get_model_path(k, adversarial, model_name)
    _loaded_agent, _ = Agent.import_agent(model_path, k)
    _state_history = StateHistory(k)
    return _loaded_agent

def get_state(k: int, table_cards: list[int], opp_table_cards: list[int], omit_player_0_last: bool) -> State:
    if omit_player_0_last:
        table_cards = table_cards[:-1]
    state = State(k, tuple([card - 1 for card in table_cards]), tuple([card - 1 for card in opp_table_cards]))
    return state

def play_card(k: int, table_cards: list[int], opp_table_cards: list[int]) -> int:
    global _state_history
    state = get_state(k, table_cards, opp_table_cards, True)
    _state_history.push(state)
    player = Player(1, k, _loaded_agent, state.get_residual_cards(1))
    played_card = player.play(_state_history, {})
    return played_card + 1

def extract_winner(k: int, table_cards: list[int], opp_table_cards: list[int]):
    state = get_state(k, table_cards, opp_table_cards, False)
    if state.is_terminal():
        return state.get_winner()
    return None