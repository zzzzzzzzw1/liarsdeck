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
