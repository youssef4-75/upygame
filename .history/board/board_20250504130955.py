from typing import Callable, Iterable, TypeVar
import pygame as pg 
from multipledispatch import dispatch

from utilities import init_method, loop_method, limit_calls, SideAlreadySetError

from .peace import Peace




class Board:
    def __init__(self, row: int, column: int,
                cell_width: int=100, 
                cell_height: int=100,
                init_pos: tuple[int, int] = (0, 0),
                style: Callable[[int, int], 
                            tuple[int, int, int]] 
                            = lambda x, y: (0, 0, 0)):
        self.shape = (row, column)
        self.cell_shape = (cell_width, cell_height)
        self.init_pos = init_pos
        self.style = style
        self.peaces = set()
        self.sides = []
        self.turn = None

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
   
    @property
    def top(self):
        return self.init_pos[0]
   
    @property
    def left(self):
        return self.init_pos[1]

    def get_cell(self, row: int, 
                    column: int, 
                ) -> tuple[pg.Rect, tuple[int, int, int]]:
        """Get the cell rectangle."""
        x = column * self.cell_width + self.left
        y = row * self.cell_height + self.top
        return pg.Rect(x, y, self.cell_width, self.cell_height), self.style(row, column)

    @staticmethod
    def __tr(coordinate: int, offset: int, cell_size: int):
        return (coordinate - offset) // cell_size

    @loop_method
    def translate_mouse_click(self, mouse_pos):
        return (Board.__tr(mouse_pos[0], self.left, 
                        self.cell_width),
                Board.__tr(mouse_pos[1], self.top, 
                        self.cell_height))
    
    def activate_drag(self, mouse_pos):...

    def add_side(self, side: int):
        self.sides.append(side)
        if self.turn is None:
            self.turn = side 

    def __add_1p(self, peace: Peace):
        self.peace.add(peace)

    def add_peace(self, side: int, *peaces: Peace):
        if side in self.sides: 
            raise SideAlreadySetError(side, self.sides)
        self.add_side(side)
        for peace in peaces: 
            peace.set_side(side)
            self.__add_1p(peace)



