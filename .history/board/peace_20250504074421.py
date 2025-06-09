

class Peace:
    def __init__(self, board):
        self.board = board
        self.pieces = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0
        }

    def evaluate(self):
        score = 0
        for row in self.board:
            for piece in row:
                score += self.pieces.get(piece, 0)
        return score