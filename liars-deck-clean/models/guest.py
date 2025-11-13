# from app import db
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
    
    def to_dict(self):
        return {
            "name":self.name,
            "is_ready": self.is_ready,
            "wins": self.wins,
            "losses": self.losses
        }