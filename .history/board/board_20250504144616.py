from typing import Callable, Iterable, TypeVar
import pygame as pg 
from multipledispatch import dispatch

from utilities import (init_method, loop_method, 
        limit_calls, SideAlreadySetError,
        MoveCollisionError, OPPSelected
                       )

from .peace import Peace
from .var import Column_X, Row_Y




class Board:
    def __init__(self, row: Row_Y, column: Column_X,
                cell_width: Column_X=100, 
                cell_height: Row_Y=100,
                init_pos: tuple[Row_Y, Column_X] = (0, 0),
                style: Callable[[int, int], 
                            tuple[int, int, int]] 
                            = lambda x, y: (0, 0, 0)):
        self.shape = (Row_Y(row), Column_X(column))
        self.cell_shape = (Column_X(cell_width), Row_Y(cell_height))
        self.init_pos = (Row_Y(init_pos[0]), Column_X(init_pos[1]))
        self.style = style
        self.peaces: set[Peace] = set()
        self.peace_in_focus = None
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
    def bottom(self):
        return self.left + self.height
    
    @property
    def left(self):
        return self.init_pos[1]

    @property
    def right(self):
        return self.left + self.width
    
    @property
    def width(self):
        return self.column * self.cell_width

    @property
    def height(self):
        return self.row * self.cell_heightwidth

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
    
    @loop_method
    def activate_peace(self, mouse_pos: tuple[Column_X, Row_Y]) -> Peace:
        """
        after clicking in a cell, this function return the peace you selected, it just should be yours
        """
        if self.peace_in_focus is not None: raise MoveCollisionError()
        row, column = self.translate_mouse_click(mouse_pos)
        for peace in self.peaces:
            if peace.row == row and peace.column == column:
                if peace.side != self.turn: raise OPPSelected(peace)
                self.peace_in_focus = peace
                return peace
        raise Exception("no peaces are here")

    @loop_method
    def update(self):
        self.peace_in_focus.update(self)

    @loop_method
    def release(self):
        self.peace_in_focus = None 

    def __add_side(self, side: int):
        self.sides.append(side)
        if self.turn is None:
            self.turn = side 

    def __add_1p(self, peace: Peace):
        self.peace.add(peace)

    @init_method
    def add_peace(self, side: int, *peaces: Peace):
        if side in self.sides: 
            raise SideAlreadySetError(side, self.sides)
        self.__add_side(side)
        for peace in peaces: 
            peace.set_side(side)
            self.__add_1p(peace)

    def draw(self, window):




