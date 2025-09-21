class Cell:
    def __init__(self, button):
        self.button = button
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mine_counter = 0