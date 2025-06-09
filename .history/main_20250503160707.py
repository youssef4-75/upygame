import pygame as pg 

from window import Window
from loops import loop1
from animation import AnimationSet, Animation

win = Window("Test", 800, 600, loop1)
win.white()
win.add_params()


S = pg.Surface((100, 100), pg.SRCALPHA)
S.fill((255, 0, 0))

S = pg.Surface((100, 100), pg.SRCALPHA)
S.fill((255, 255, 0))

A1 = Animation()



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


