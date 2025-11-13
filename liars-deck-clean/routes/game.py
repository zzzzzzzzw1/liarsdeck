from flask import Blueprint, jsonify
from routes.lobby import lobby

game_blueprint = Blueprint("game", __name__)

@game_blueprint.route("/game/status", methods=["GET"])
def get_status():
    if lobby.game == None:
        return jsonify({"error": "No active game" }), 400
    
    return jsonify({
        "ongoing": lobby.game.status_update(),
        "num_players": lobby.game.num_players,
        "players_alive": [player.name for player in lobby.game.players]
    })

@game_blueprint.route("/game/winner", methods=["POST"])
def get_winner():
    if lobby.game is None:
        return jsonify({"error": "game not found"})
    
    if lobby.game.ongoing:
        return jsonify({"message": "Game is still in progress"}), 400
    
    return jsonify({"winner": lobby.game.get_winner()})
