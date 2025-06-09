from typing import Callable
import pygame as pg 

from ..utilities import (init_method, loop_method, 
        SideAlreadySetError,
        MoveCollisionError, OPPSelected
                       )

from .piece import Piece
from .var import Column_X, Row_Y
from .phase import Phase
from .exception import FinalRepException




class Board:
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)
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
        self.pieces: list[Piece] = []
        self.piece_in_focus = None
        self.sides = []
        self.turn = None
        self.__game_phases: list[Phase] = []
        self.__cp = 0

    def __getitem__(self, index: int):
        return self.pieces[index]
 
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
        return self.top + self.height
    
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
        return self.row * self.cell_height

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
    
    def __contains__(self, piece: Piece):
        return piece in self.pieces
    
    @loop_method
    def draw_piece(self, win, piece: Piece, *, overflow: bool = True):
        row, column = piece.row, piece.column
        if not overflow and (row < 0 or row >= self.row or column < 0 or column >= self.column):
            return
        rect, _ = self.get_cell(row, column)
        if piece.image: piece.image = pg.transform.scale(piece.image, (rect.width, rect.height))
        win.blit(piece.image or pg.Surface((rect.width, rect.height)), rect)

    @loop_method
    def translate_mouse_click(self, mouse_pos):
        return (Board.__tr(mouse_pos[0], self.left, 
                        self.cell_width),
                Board.__tr(mouse_pos[1], self.top, 
                        self.cell_height))
    
    @loop_method
    def activate_piece(self, mouse_pos: tuple[Column_X, Row_Y]) -> Piece:
        """
        after clicking in a cell, this function return the piece you selected, it just should be yours
        """
        if self.piece_in_focus is not None: raise MoveCollisionError()
        row, column = self.translate_mouse_click(mouse_pos)
        for piece in self.pieces:
            if piece.row == row and piece.column == column:
                if piece.side != self.turn: raise OPPSelected(piece)
                self.piece_in_focus = piece
                return piece
        raise Exception("no pieces are here")

    @loop_method
    def update(self):
        if self.piece_in_focus is not None:
            self.piece_in_focus.update(self)

    @loop_method
    def release(self):
        self.piece_in_focus = None 

    def __add_side(self, side: int):
        self.sides.append(side)
        if self.turn is None:
            self.turn = side 

    def __add_1p(self, piece: Piece):
        self.pieces.append(piece)

    @init_method
    def add_piece(self, side: int, *pieces: Piece):
        if side in self.sides: 
            raise SideAlreadySetError(side, self.sides)
        self.__add_side(side)
        for piece in pieces: 
            piece.set_side(side)
            self.__add_1p(piece)

    @init_method
    def add_phase(self, query, window):
        self.__game_phases.append(Phase.from_query(query, window, self))

    def execute(self, window):
        if not self.__game_phases: return
        try: 
            self.__game_phases[self.__cp](window, self)
        except FinalRepException:
            self.end_phase()

    def end_phase(self):
        self.__cp += 1
        if self.__cp >= len(self.__game_phases):
            self.__cp = 0
            self.turn = self.sides[(self.turn + 1)%len(self.sides)]
        self.__game_phases[self.__cp].init_phase()