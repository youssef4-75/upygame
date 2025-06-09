import pygame as pg 

from window import Window
from loops import loop1
from board import *
from test import TPiece


win = Window("Test", 800, 640, loop1)
win.add_params()

board = Board(8, 8, init_pos=(0, 0), cell_width=100, cell_height=80)

phase1 = """
mm F KEY k  -> 
PEACE[0].move(UP)
if PEACE[0].row == 0: 
    END"""
phase2 = """
2 T KEY f || MOUSE 2 ->
PEACE[0].move(DOWN)
"""

board.add_phase(phase1, win)
board.add_phase(phase2, win)

surf = pg.Surface((100, 100))   
surf.fill((255, 0, 0))

board.add_piece(0, TPiece(4, 0, surf))

while win.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            win.running = False
            

    # start of the game loop
    win.heading()
    


    # game logic here
    win.loop()
    board.execute(win)
    win.blit(board, limits=True, color=3*(255,), overflow=True)

    

    # end of the game loop
    win.tailing()


