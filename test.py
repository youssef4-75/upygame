from board import Piece


class TPiece(Piece):
    def __init__(self, row, column, image=None):
        super().__init__(row, column, image)

    def update(self, board):
        ...


