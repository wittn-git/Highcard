from backend.src.options import list_card_counts, list_model_options
from backend.src.model_handler import play_card, extract_winner, load_model

from flask import Blueprint, jsonify, request

routes = Blueprint("routes", __name__)

@routes.route("/options/cards", methods=["GET"])
def get_card_options():
    card_options = list_card_counts()
    return jsonify(card_options)

@routes.route("/options/models", methods=["GET"])
def get_model_options():
    cards_param = request.args.get("cards", type=int)
    if cards_param is None:
        return jsonify({"error": "Missing 'cards' query parameter"}), 400
    models = list_model_options(cards_param)
    return jsonify(models)

@routes.route("/play", methods=["GET", "POST"])
def get_card():
    data = request.get_json()
    card_value = play_card(data["cardCount"], data["tableCards"], data["oppTableCards"])
    return jsonify({"status": "ok", "card": card_value})

@routes.route("/modelload", methods=["POST"])
def set_model():
    data = request.get_json()
    load_model(data["model"], data["cardCount"])
    return jsonify({"status": "ok"})

@routes.route("/winner", methods=["GET", "POST"])
def get_winner():
    data = request.get_json()
    winner = extract_winner(data["cardCount"], data["tableCards"], data["oppTableCards"])
    if winner == None:
        return jsonify({"status": "ok"})
    winner_map = {0: "Human", 1: "AI", -1: "Tie"}
    return jsonify({"status": "ok", "winner": winner_map[winner]})