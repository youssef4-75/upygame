from typing import Callable, Iterable, TypeVar
import pygame as pg 
from multipledispatch import dispatch

from utilities import (init_method, loop_method, 
        limit_calls, SideAlreadySetError,
        MoveCollisionError, OPPSelected
                       )

from .peace import Peace
from .var import Column_X, Row_Y






class SpBoard:
    def __init__(self, source, special_area: Iterable[pg.Rect], init_pos: tuple[Row_Y, Column_X]):
        self.__source = source
        self.init_pos = init_pos
        self.__area = special_area
        self.peaces: set[Peace] = set()
        self.peace_in_focus = None
        self.sides = []
        self.turn = None
    
    def __len__(self):
        return len(self.__area)
    
   
    def get_cell(self, index: int
                ) -> tuple[pg.Rect, tuple[int, int, int]]:
        """Get the cell rectangle."""
        return self.__area[index]

    @loop_method
    def translate_mouse_click(self, mouse_pos):
        for i, rect in enumerate(self.__area):
            if rect.collidepoint(mouse_pos):
                return i
        return 
        
    
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


