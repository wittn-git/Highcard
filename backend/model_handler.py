def get_card(model, card_count, table_cards, opp_table_cards) -> int:
    # TODO implement model handler logic
    playable_cards = [i for i in range(1, card_count+1) if i not in opp_table_cards]
    return max(playable_cards)