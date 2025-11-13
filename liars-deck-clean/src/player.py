class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.alive = True
        self.max_lives = 6
        self.instructions = True
    
    def eliminate(self):
        self.alive = False
        print(str(self.name) + " has been eliminated!")
        
    def display_name(self):
        shots_taken = abs(self.max_lives - 6)
        return f"{self.name} [{shots_taken}/6]"
    