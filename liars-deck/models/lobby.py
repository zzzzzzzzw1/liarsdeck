from models.guest import Guest
from models.game import Game
class Lobby:
    def __init__(self):
        self.guests = []   # List of players in the lobby
        self.game = None
        self.games = []     # List of completed games
        
    def add_guest(self, guest):
        # Adds a new player to the lobby
        if len(self.guests) == 4:
            # print("Maximum Lobby Size. Cannot add anymore players.")
            return {"error": "Lobby is full"}
        if guest in self.guests:
            # print("ERROR: Name already taken. Please try a new name")
            return {"error": "Name already taken. Please try a new name."}
        self.guests.append(guest)
        
        return {"message": f"{guest.name} has joined the lobby."}
        # print("{guest} has joined the lobby.".format(guest = guest.name))
    
    def remove_guest(self, guest_name):
        # Player removed by the lobby creator
        # Might need case where they can't remove themselves otherwise that will cause error
        for guest in self.guests:
            if guest_name == guest.name:
                self.guests.remove(guest)
                return {"message": f"{guest_name} has been removed from the lobby"}
        else:
            return {"error": "Guest to remove doesn't exist"}
            # print("ERROR: Guest to remove doesn't exist")
    
    def guest_leave(self, guest):
        # Guests leaving on their own accord
        if guest in self.guests:
            self.guests.remove(guest)
            print("{guest} has left the lobby.".format(guest = guest.name))
        else:
            print("ERROR: Leaving guest doesn't exist")
        
    def all_ready(self):
        for guest in self.guests:
            if guest.is_ready == False:
                return False
        return True
    
    def start_game(self):
        if not self.all_ready():
            # print("Not all guests are ready. Cannot start the game.")
            return {"error": "Not all guests are ready. Cannot start the game"}
        
        if len(self.guests) <= 1:
            # print("Cannot start game with just one player.")
            return {"error": "Cannot start game with just one player"}
            
        g = Game(self.guests)
        winner = g.get_winner()
        self.increment_win(winner)
        return {"message": "Welcome to Liar's Deck!"}
    
    def view_lobby(self):
        print("______LOBBY_______")
        for guest in self.guests:
            print(f"{guest.name}: {guest.wins} wins\n")
        print("__________________")
        
    def increment_win(self, player_name):
        for guest in self.guests:
            if player_name == guest.name:
                guest.wins += 1
            else:
                guest.losses += 1
                
    def to_dict(self):
        return {
            "players": [guest.to_dict() for guest in self.guests]
        }
        
    def toggle_ready(self, player_name):
        for guest in self.guests:
            if guest.name == player_name:
                guest.toggle_ready()
                return {"message": f"{player_name} is now {'ready' if guest.is_ready else 'not ready'}"}
        return {"error": "Player not found"}