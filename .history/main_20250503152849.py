import pygame as pg 

from window import Window
from loops import loop1
from animation import AnimationSet

win = Window("Test", 800, 600, loop1)
win.white()
win.add_params()


AS = 
S = pg.Surface((100, 100), pg.SRCALPHA)
S.fill((255, 0, 0))
win.blit(S, (1, 1))

while win.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            win.running = False
            

    # start of the game loop
    win.heading()


    # game logic here
    win.loop()

    # end of the game loop
    win.tailing()


