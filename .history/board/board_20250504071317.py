import pygame as pg 
pg.draw.re

class Board:
    def __init__(self, row: int, column: int,
                cell_width: int=100, 
                cell_height: int=100):
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
    


    