from training.agents.agent import Agent
from training.agents.agent_DQN import DQNAgent
from training.agents.agent_PI import TabularAgent
from training.agents.agent_STRAT import StrategyAgent
from training.util.classes import GameHistory, Player, State
from backend.options import MODEL_MAPPING

from typing import Callable
import os

_loaded_model_name, _loaded_strategy = None, None

def load_model(model_name : str, k : int) -> Callable[[Player, GameHistory], int]:
    global _loaded_model_name, _loaded_strategy
    if _loaded_model_name != model_name:
        _loaded_model_name = model_name
        agent, _ = Agent.import_agent(f"training/models/{MODEL_MAPPING[k][_loaded_model_name]}", k)
        _loaded_strategy = agent.get_strategy()
    return _loaded_strategy

def get_gamehistory(table_cards : list[int], opp_table_cards : list[int], omit_player_0_last : bool) -> GameHistory:
    if omit_player_0_last:
        table_cards = table_cards[:-1]
    state = State(tuple([card - 1 for card in table_cards]), tuple([card - 1 for card in opp_table_cards]))
    game_history = GameHistory(state)
    return game_history

def get_card(model_name : str, k : int, table_cards : list[int], opp_table_cards : list[int]) -> int:
    strategy = load_model(model_name, k)
    game_history = get_gamehistory(table_cards, opp_table_cards, True)
    player = Player(1, k, strategy, game_history.get_state().get_residual_cards(1, k))
    played_card = strategy(player, game_history, {"player_id": 1})
    return played_card + 1

def extract_winner(k : int, table_cards : list[int], opp_table_cards : list[int]):
    game_history = get_gamehistory(table_cards, opp_table_cards, False)
    state = game_history.get_state()
    if state.is_terminal(k):
        return state.get_game_winner()
    return None