from typing import Callable
import pygame as pg 


class Board:
    def __init__(self, row: int, column: int,
                cell_width: int=100, 
                cell_height: int=100,
                style: Callable[[int, int], tuple[int, int, int]]] = lambda x, y: (0, 0, 0)):
        self.shape = (row, column)
        self.cell_shape = (cell_width, cell_height)

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
    
    def draw(self, window: pg.Surface, color: tuple[int, int, int]):
        for i in range(self.row):
            for j in range(self.column):
                x = j * self.cell_width
                y = i * self.cell_height
                rect = pg.Rect(x, y, self.cell_width, self.cell_height)
                pg.draw.rect(window, color, rect, 1)
    


    