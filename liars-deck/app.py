from flask import Flask, render_template
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy

from routes.lobby import lobby_blueprint
from routes.game import game_blueprint
from routes.player import player_blueprint

app = Flask(__name__) 
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liarsbar.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

app.register_blueprint(lobby_blueprint, url_prefix="/api")
app.register_blueprint(game_blueprint, url_prefix="/api")
app.register_blueprint(player_blueprint, url_prefix="/api")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lobby')
def lobby_page():
    return render_template('lobby.html')

@app.route('/game')
def game_page():
    return render_template('game.html')

if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)
    