class PostingList:
    positions = None  # type: [int]

    def __init__(self, position):
        self.positions = [position]

    def get_positions(self):
        return self.positions

    def add_position(self, position):
        self.positions.append(position)
