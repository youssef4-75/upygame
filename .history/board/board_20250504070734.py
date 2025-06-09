

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def display(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

    def place_piece(self, x, y, piece):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.board[x][y] = piece
        else:
            raise ValueError("Position out of bounds")