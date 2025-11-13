from flask import Blueprint, request, jsonify
from models.lobby import Lobby
from models.guest import Guest

lobby_blueprint = Blueprint("lobby", __name__)

lobby = Lobby()

@lobby_blueprint.route("/lobby/join", methods=["POST"])
def join_lobby():
    data = request.get_json()
    
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request, 'name' is required"}), 400
        
    guest = Guest(data["name"])
    result = lobby.add_guest(guest)
    return jsonify(result)

@lobby_blueprint.route("/lobby/leave", methods=["POST"])
def leave_lobby():
    data = request.get_json()
    
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request, 'name' is required"}), 400
    
    result = lobby.remove_guest(data["name"])
    return jsonify(result)

@lobby_blueprint.route("/lobby/ready", methods=["POST"])
def toggle_ready():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid request, 'name' is required"}), 400
    result = lobby.toggle_ready(data["name"])
    return jsonify(result)

@lobby_blueprint.route("/lobby/status", methods=["GET"])
def lobby_status():
    return jsonify(lobby.to_dict())

@lobby_blueprint.route("/lobby/start", methods=["POST"])
def start_game():
    result = lobby.start_game()
    return jsonify(result)