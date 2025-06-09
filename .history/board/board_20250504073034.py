from typing import Callable
import pygame as pg 
from multipledispatch import dispatch


class Board:
    def __init__(self, row: int, column: int,
                cell_width: int=100, 
                cell_height: int=100,
                style: Callable[[int, int], tuple[int, int, int]] = lambda x, y: (0, 0, 0)):
        self.shape = (row, column)
        self.cell_shape = (cell_width, cell_height)
        
        self.style = style

    @property
    def row(self):
        return self.shape[0]
    
    @property
    def column(self):
        return self.shape[1]

    @property
    def cell_width(self):
        return self.cell_shape[0]
    
    @property
    def cell_height(self):
        return self.cell_shape[1]

    def __getitem__(self, index: tuple[int, int]):
        return 

    