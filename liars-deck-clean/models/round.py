from models.turn import Turn
import random
import time

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
        if symbol == "ace":
            return "Ace" + ("s" if amount > 1 else "")
        elif symbol == "king":
            return "King" + ("s" if amount > 1 else "")
        elif symbol == "queen":
            return "Queen" + ("s" if amount > 1 else "")
        elif symbol == "joker":
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
        draw = ["ace", "king", "queen"]
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
        deck = ['ace'] * 6 + ['king'] * 6 + ['queen'] * 6 + ['joker'] * 2
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