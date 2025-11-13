from models.player import Player
from models.round import Round
class Game:
    def __init__(self, guests):
        self.players = [Player(guest.name) for guest in guests]
        self.num_players = len(self.players)
        self.ongoing = True
        self.winner = None
        self.play_game()
        
    def play_game(self):
        while self.ongoing == True:
            # Keeps track of the round and also continues initiating Round class as long 
            # as game status is True / Ongoing
            Round(self.players)
            self.status_update()
        # Once game status toggles to false we will close the game and 
        # award victory to the last remaining player
        self.winner = self.players[0]
        return
    
    def get_winner(self):
        return self.winner.name
    
    def status_update(self):
        self.players = [player for player in self.players if player.alive]
        self.num_players = len(self.players)
        if self.num_players == 1:
            self.ongoing = False
            
        return {
            "ongoing": self.ongoing,
            "num_players": self.num_players,
            "players_alive": [player.name for player in self.players]
        }