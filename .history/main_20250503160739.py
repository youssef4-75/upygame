import pygame as pg 

from window import Window
from loops import loop1
from animation import Animation

win = Window("Test", 800, 600, loop1)
win.white()
win.add_params()


S1 = pg.Surface((100, 100), pg.SRCALPHA)
S1.fill((255, 0, 0))

S2 = pg.Surface((100, 100), pg.SRCALPHA)
S2.fill((255, 255, 0))

A1 = Animation(S1)
A2 = Animation(S2)
 A1 + A2



while win.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            win.running = False
            

    # start of the game loop
    win.heading()


    # game logic here
    win.loop()
    win.blit(AS, (1, 1, 10, 10), state=1)

    # end of the game loop
    win.tailing()


