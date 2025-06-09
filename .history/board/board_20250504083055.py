from typing import Callable
import pygame as pg 
from multipledispatch import dispatch


class Board:
    def __init__(self, row: int, column: int,
                cell_width: int=100, 
                cell_height: int=100,
                style: Callable[[int, int], 
                            tuple[int, int, int]] 
                            = lambda x, y: (0, 0, 0)):
        self.shape = (row, column)
        self.cell_shape = (cell_width, cell_height)

        self.style = style
        self.peaces = {}

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

    @dispatch(int, int, tuple)
    def get_cell(self, row: int, 
                    column: int, 
                    init_pos: tuple[int, int] = (0, 0),
                ) -> tuple[pg.Rect, tuple[int, int, int]]:
        """Get the cell rectangle."""
        x = column * self.cell_width + init_pos[0]
        y = row * self.cell_height + init_pos[1]
        return pg.Rect(x, y, self.cell_width, self.cell_height), self.style(row, column)

    @dispatch(int, int, tuple)
    def get_cell(self, row: int,
                    column: int, 
                    init_pos: pg.Rect, 
                ) -> tuple[pg.Rect, tuple[int, int, int]]:
        """Get the cell rectangle."""
        return self.get_cell(row, column, (init_pos.left, init_pos.top))

    @staticmethod
    def 

    def translate_mouse_click(self, mouse_pos, my_pos):
        ...