from util.classes import Card, GameHistory, Player
from util.playing import play_round

from typing import List, Tuple, Callable
from itertools import product
import random
from prettytable import PrettyTable

class DQNAgent:

    def __init__(self, starting_cards : List[Card]):
        super().__init__(starting_cards)