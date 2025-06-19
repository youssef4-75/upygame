"""
Piece module for abstract game pieces on the board.

This module provides the Piece abstract base class for representing game pieces.
It defines the interface and common properties for all pieces used on a board.
"""

from abc import ABC, abstractmethod
from pygame import Surface

from ..utilities import limit_calls

from .var import Column_X, Row_Y



class Piece(ABC):
    """
    Abstract base class for a game piece.
    
    This class defines the interface and common properties for all game pieces.
    Subclasses must implement the update method.
    
    Attributes:
        __pos (list): Position of the piece (row, column)
        __side: Side or player the piece belongs to
        image (Surface|None): Visual representation of the piece
    """
    def __init__(self, row: int,
                column: int,
                image: Surface = None):
        self.__pos = [row, column]
        self.__side = None
        if isinstance(image, str):
            image = image.load(image)
        self.image = image
        super().__init__()
       
    @property
    def side(self):
        return self.__side 
    
    @property
    def row(self) -> int|Row_Y:
        return self.__pos[0]

    @property
    def column(self) -> int|Column_X:
        return self.__pos[1]
   
    @limit_calls(1)
    def set_side(self, side) -> None:
        self.__side = side

    def move(self, step: tuple[int, int]):
        self.__pos[0] += step[0]
        self.__pos[1] += step[1]
    
    @abstractmethod
    def update(self, board): ...
    

    
    

    

