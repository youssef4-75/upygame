

from typing import Iterable


class Peace:
    def __init__(self, row: int,
                column: int, side, 
                valid_moves: Iterable[tuple[int, int]]):
        self.__pos = [row, column]
        self.__side = side
        self.__valid_moves = valid_moves

    @property
    def side(self):
        return self.__side 
    
    @property
    def x(self):
        return self.__pos[0]

    @property
    def y(self):
        return self.__pos[1]
    
    @property
    def valid_cell(self):
        for i, j in self.__valid_moves:
            yield self.x + i, self.
    

    


    