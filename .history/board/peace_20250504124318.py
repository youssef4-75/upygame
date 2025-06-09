

from typing import Iterable


class Peace:
    def __init__(self, row: int,
                column: int, side, 
                valid_moves: Iterable[tuple[int, int]]):
        self.__pos = [row, column]
        self.__side = side
        self.__valid_moves = sorted(valid_moves, lambda item:item[0])

       

    @property
    def side(self):
        return self.__side 
    
    @property
    def row(self):
        return self.__pos[0]

    @property
    def column(self):
        return self.__pos[1]
    
    @property
    def valid_cell(self):
        for i, j in self.__valid_moves:
            yield self.row + i, self.column + j

    def validate(self, move_to_cell: tuple[int, int]):
        
    
    

    


    