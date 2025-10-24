from backend.options import CARD_OPTIONS, MODEL_OPTIONS
from backend.model_handler import get_card, extract_winner

from flask import Blueprint, jsonify, request

routes = Blueprint("routes", __name__)

@routes.route("/options/cards", methods=["GET"])
def get_card_options():
    return jsonify(CARD_OPTIONS)

@routes.route("/options/models", methods=["GET"])
def get_model_options():
    cards_param = request.args.get("cards", type=int)
    if cards_param is None:
        return jsonify({"error": "Missing 'cards' query parameter"}), 400
    models = MODEL_OPTIONS[cards_param]
    return jsonify(models)

@routes.route("/play", methods=["GET", "POST"])
def play_card():
    data = request.get_json()
    model, table_cards, opp_table_cards, card_count = data["model"], data["tableCards"], data["oppTableCards"], data["cardCount"]
    card_value = get_card(model, card_count, table_cards, opp_table_cards)
    return jsonify({"status": "ok", "card": card_value})

@routes.route("/winner", methods=["GET", "POST"])
def get_winner():
    data = request.get_json()
    table_cards, opp_table_cards, card_count = data["tableCards"], data["oppTableCards"], data["cardCount"]
    winner = extract_winner(card_count, table_cards, opp_table_cards)
    if winner == None:
        return jsonify({"status": "ok"})
    winner_map = {0: "Human", 1: "AI", -1: "Tie"}
    return jsonify({"status": "ok", "winner": winner_map[winner]})