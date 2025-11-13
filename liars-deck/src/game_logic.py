import random
import time
from player import Player

class Guest:
    def __init__(self, display_name):
        self.name = display_name
        self.is_ready = False
        self.wins = 0
        self.losses = 0
        
    def toggle_ready(self):
        # Have a button for each guest that 
        # they can press to toggle their ready status
        self.is_ready = not self.is_ready
        return self.is_ready

    def __repr__(self):
        return f"Guest(display_name={self.name}, is_ready={self.is_ready})"
        
class Lobby:
    def __init__(self):
        self.guests = []   # List of players in the lobby
        self.game = None
        self.games = []     # List of completed games
        
    def add_guest(self, guest):
        # Adds a new player to the lobby
        if len(self.guests) == 4:
            print("Maximum Lobby Size. Cannot add anymore players.")
            return False
        if guest in self.guests:
            print("ERROR: Name already taken. Please try a new name")
            return False
        self.guests.append(guest)
        print("{guest} has joined the lobby.".format(guest = guest.name))
    
    def remove_guest(self, guest):
        # Player removed by the lobby creator
        # Might need case where they can't remove themselves otherwise that will cause error
        if guest in self.guests:
            self.guests.remove(guest)
            print("{guest} has been removed from the lobby.".format(guest = guest.name))
        else:
            print("ERROR: Guest to remove doesn't exist")
    
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
            print("Not all guests are ready. Cannot start the game.")
            return False
        
        if len(self.guests) <= 1:
            print("Cannot start game with just one player.")
            return False
            
        g = Game(self.guests)
        winner = g.get_winner()
        self.increment_win(winner)
        return True 
    
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
        return True

class Round:
    def __init__(self, players):
        self.players = players
        self.ongoing = True
        self.playcard = self.initialise_playcard()
        self.initialise_hands()
        self.previous_hand = None
        self.previous_player = None
        self.play_round()
        
    def symbol_to_word(self, symbol, amount):
        if symbol == "A":
            return "Ace" + ("s" if amount > 1 else "")
        elif symbol == "K":
            return "King" + ("s" if amount > 1 else "")
        elif symbol == "Q":
            return "Queen" + ("s" if amount > 1 else "")
        elif symbol == "J":
            return "Joker" + ("s" if amount > 1 else "")

    def play_round(self):
        while self.ongoing == True:
            for player in self.players:
                if len(player.hand) == 0:
                    continue
        
                t = Turn(player)
                action = t.get_action(self.previous_hand)
                if action != 'B' and not self.last_player():
                    amount = len(action)
                    print(f"{player.name}: {amount} {self.symbol_to_word(self.playcard, amount)}!")
                    self.previous_hand = action
                    self.previous_player = player
                else: 
                    self.call_bluff(player, self.previous_player)
                    break
                    
    def last_player(self):
        return sum(1 for player in self.players if len(player.hand) > 0) <= 1
        
    def initialise_playcard(self):
        draw = ["A", "K", "Q"]
        round_card = random.choice(draw)
        print("______________")
        print(f"{self.symbol_to_word(round_card, 1)}'s Table!")
        print("______________")
        
        return round_card
       
    ## def start_turn_timer(self, player):
        time.sleep(30)
        self.call_bluff(player, self.previous_player)
        pass

    def initialise_hands(self):
        # Randomly distributes 5 cards to each of the players from a deck of
        # 6 Kings, 6 Aces, 6 Queens, 2 Jokers
        deck = ['A'] * 6 + ['K'] * 6 + ['Q'] * 6 + ['J'] * 2
        random.shuffle(deck)
        
        for player in self.players:
            player.hand = [deck.pop() for _ in range(5)]

        print("There are 6 Aces, 6 Kings, 6 Queens and 2 Jokers in the deck.")
    
    def roulette(self, player):
        bullet_chamber = random.randint(1, player.max_lives)
        shot = random.randint(1, player.max_lives)
        print("Waiting...")
        time.sleep(4)
        
        if shot == bullet_chamber:
            print("The chamber contained a bullet!")
            player.eliminate()
        else:
            print("The chamber was empty! " + str(player.name) + " lives another day!")
            player.max_lives -= 1 
        
        self.ongoing = False   
    
    def call_bluff(self, current_player, previous_player):
        print("LIAR!")
        print(f"The previous hand was: " + str(self.previous_hand))
        correct_hands = self.generate_valid_hands(self.playcard, len(self.previous_hand))
        
        if self.previous_hand in correct_hands:
            self.roulette(current_player)
            return False # Incorrect bluff call
        
        self.roulette(previous_player)
        return True # Correct bluff call, previous hand was a bluff!
            
    def generate_valid_hands(self, playcard, hand_size):
        from itertools import product
        
        possible_cards = [playcard, 'J']
        
        valid_hands = product(possible_cards, repeat=hand_size)
        
        return [list(hand) for hand in valid_hands]
        
class Turn:
    def __init__(self, player):
        self.player = player
        self.print_instructions()

    def print_instructions(self):
        if self.player.instructions == True:
            print(f"CURRENT PLAYER: {self.player.display_name()}")
            
            ## print("It is now your turn!")
            ## print("Enter B to call Bluff.")
            ## print("Enter the index 1 - 5 of the cards you want to play separated by just a comma")
            ## print("For example if your hand is [K, K, Q, J, Q] you may enter '1,2' to play two cards which are") 
            ## print("your first and second cards which both Kings or something like '3' to play your 3rd card (Queen)")
            ## print("Enter I to toggle the instruction display.")
        
        self.print_hand()
        
    def print_hand(self):
        print("Your hand is:")
        counter = 1
        for card in self.player.hand:
            print(f"{counter}. {card}")
            counter += 1
    
    def get_action(self, previous_hand):
        while True:
            user_input = input("Enter your action: ").upper()
            
            if user_input == 'B':
                if previous_hand == None:
                    print("Cannot call bluff on first turn!")
                    continue
                return user_input
                # Call Bluff
            elif user_input == 'I':
                self.player.instructions = not self.player.instructions
                state = "on" if self.player.instructions else "off"
                print(f"Instructions are now turned {state}.")
                continue
            
            else: 
                try: 
                    inputs = [int(i.strip()) for i in user_input.split(",")]
                except ValueError:
                    print("ERROR: Please enter valid integers separated by commas.")
                    continue
                
                if self.validate_indices(inputs):
                    play_cards = [self.player.hand[i - 1] for i in inputs]
                    for card in play_cards:
                        self.player.hand.remove(card)
                    return play_cards
                else: 
                    continue
    
    def validate_indices(self, indices):
        if len(indices) > 3:
            print("ERROR: Cannot play more than 3 cards")
            return False
        if any(i < 1 or i > len(self.player.hand) for i in indices):
            print("ERROR: Index out of the range of the player's hand!")
            return False
        if len(set(indices)) != len(indices):
            print("ERROR: Please do not play duplicate indices")
            return False
        
        return True
