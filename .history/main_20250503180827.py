import pygame as pg 

from window import Window
from loops import loop1
from animation import AnimationSet

win = Window("Test", 800, 600, loop1)
win.white()
win.add_params()





while win.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            win.running = False
            

    # start of the game loop
    win.heading()


    # game logic here
    win.loop()
    
    win.blit(A, (1, 1, 10, 10), state=0)
    win.blit(A1, (1, 170, 1, 1), state=0)

    # end of the game loop
    win.tailing()


