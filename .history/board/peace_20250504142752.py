

from typing import Generator, Iterable
from abc import ABC, abstractmethod
from utilities import limit_calls, loop_method

from .var import Column_X, Row_Y

class Peace(ABC):
    def __init__(self, row: int,
                column: int,
                valid_moves: Iterable[tuple[Row_Y, Column_X]]):
        self.__pos = [row, column]
        self.__side = None
        self.__valid_moves: Iterable[tuple[Row_Y, Column_X]] = (
            sorted(valid_moves, lambda item:item[0])
        )
       
    @property
    def side(self):
        return self.__side 
    
    @property
    def row(self) -> int|Row_Y:
        return self.__pos[0]

    @property
    def column(self) -> int|Column_X:
        return self.__pos[1]
    
    @property
    def valid_cell(self) -> Generator[Row_Y, Column_X]:
        for i, j in self.__valid_moves:
            yield self.row + i, self.column + j

    @limit_calls(1)
    def set_side(self, side) -> None:
        self.__side = side

    @loop_method
    def validate(self, cell_to_move_to: tuple[Row_Y, Column_X]) -> bool:
        for i, j in self.valid_cell:
            if cell_to_move_to[0] == i and cell_to_move_to[1] == j:
                return True
            if i > cell_to_move_to[0]: 
                return False
        return False 
    

        
    
    

    


    