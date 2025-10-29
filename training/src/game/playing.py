from training.src.game.classes import Player, State, StateHistory
from training.src.agents.abstract.agent import Agent

def play_trick(player_1: Player, player_2: Player, state_history: StateHistory, show: bool = False):
    card_1 = player_1.play(state_history, {"player_id": 0})
    card_2 = player_2.play(state_history, {"player_id": 0})
    if show:
        print(card_1, card_2)
    state = state_history.pop()
    state.add_cards(card_1, card_2)
    state_history.push(state)
    # TODO revise
    return state_history

def play_round(
        k: int, 
        player_0: Player,
        player_1: Player,
        state_history: StateHistory = None,
        reset: bool = True,
        show: bool = False
    ) -> StateHistory:

    if state_history is None:
        state_history = StateHistory(k)
    else:
        state_history.push(State(k))

    for _ in range(k):
        play_trick(player_0, player_1, state_history, show)
    
    if reset:
        player_0.reset()
        player_1.reset()
        
    return state_history

def play_rounds(
        n_rounds: int, 
        k: int, 
        agent_0: Agent, 
        agent_1: Agent
    ):
    
    wins_0, wins_1, draws = 0, 0, 0

    player_0, player_1 = Player(0, k, agent_0), Player(1, k, agent_1)
    state_history = StateHistory(k)

    for _ in range(n_rounds):

        state_history = play_round(k, player_0, player_1)
        winner = state_history.top().get_winner()

        if winner == 0: 
            wins_0 += 1
        elif winner == 1: 
            wins_1 += 1
        else: 
            draws += 1

    return wins_0, wins_1, draws