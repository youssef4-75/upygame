

from typing import Iterable

from utilities import 

class Peace:
    def __init__(self, row: int,
                column: int,
                valid_moves: Iterable[tuple[int, int]]):
        self.__pos = [row, column]
        self.__side = None
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

    def set_side(self, side):
        self.__side = side
    def validate(self, cell_to_move_to: tuple[int, int]):
        for i, j in self.valid_cell:
            if cell_to_move_to[0] == i and cell_to_move_to[1] == j:
                return True
            if i > cell_to_move_to[0]: 
                return False
        return False 
    

        
    
    

    


    