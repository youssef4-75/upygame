

from typing import Generator, Iterable
from abc import ABC, abstractmethod
from pygame.sprite import DirtySprite
from utilities import limit_calls, loop_method

# from .var import Column_X, Row_Y


Column_X = type("Column_X", (int,), {})
Row_Y = type("Row_Y", (int,), {})


""
from .exceptions import MaximumCallsReachedError

def limit_calls(max_calls: int):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            # Create counter if it doesn't exist
            if not hasattr(self, '__method_call_counts'):
                self.__method_call_counts = {}

            # Initialize counter for this method
            method_name = method.__name__
            if method_name not in self.__method_call_counts:
                self.__method_call_counts[method_name] = 0

            # Check call count
            if self.__method_call_counts[method_name] >= max_calls:
                raise MaximumCallsReachedError(max_calls, method_name)

            # Increment and call
            self.__method_call_counts[method_name] += 1
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

def loop_method(method):
    return method 

def init_method(method):
    return method 

def access_limit(*names):
    def decorator(method):
        def wrapper(*args, permission=None, **kwargs):
            if permission not in names:
                raise Exception
            return method(*args, **kwargs)
        return wrapper
    return decorator 
""

class Peace(ABC, DirtySprite):
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
    
    @abstractmethod
    def update(self, board): ...
        
    

    
    

    


    