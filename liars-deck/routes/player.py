from flask import Blueprint, request, jsonify
from routes.lobby import lobby

player_blueprint = Blueprint("player", __name__)

@player_blueprint.route("/player/hand", methods=["GET"])
def get_hand():
    if lobby.game == None:
        return jsonify({"error": "No active game" }), 400
    
    name = request.args.get("name")
    
    if not name:
        return jsonify({"error": "Invalid request, 'name' is required"}), 400
    
    for player in lobby.game.players:
        if player.name == name:
            return jsonify({"hand": player.hand})
        
    return jsonify({"error": "Player could not be found"}), 400

@player_blueprint.route("/player/eliminate", methods=["POST"])
def eliminate():
    if lobby.game == None:
        return jsonify({"error": "No active game" }), 400
    
    data = request.get_json()
    
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request, 'name' is required"}), 400
    
    for player in lobby.game.players:
        if player.name == data["name"]:
            return jsonify(player.eliminate())
    
    return jsonify({"error": "Player could not be found"}), 400