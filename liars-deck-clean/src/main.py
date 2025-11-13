from game_logic import Lobby, Guest, Game, Round, Turn
from player import Player

def setup_lobby():
    lobby = Lobby()
    print("Liars Bar")
    while True:
        print("Setup Lobby:")
        print("1. Add Guest")
        print("2. Remove Guest")
        print("3. Start Game")
        print("4. View Lobby")
        print("5. Exit")
        
        choice = input("Enter a command: ")
        
        if choice == "1":
            name = input("Enter username: ")
            g = Guest(name)
            g.toggle_ready()
            lobby.add_guest(g)
        elif choice == "2":
            name = input("Enter guest to remove: ")
            g = next((guest for guest in lobby.guests if guest.name == name), None)
            lobby.remove_guest(g)
        elif choice == "3":
            lobby.start_game()
        elif choice == "4":
            lobby.view_lobby()
        elif choice == "5":
            print("Lobby closed.")
            exit(0)
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    lobby = setup_lobby()