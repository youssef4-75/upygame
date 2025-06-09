import pygame as pg 

from window import Window
from loops import loop1
from animation import AnimationSet

win = Window("Test", 800, 600, loop1)
win.white()
win.add_params()


S1 = pg.Surface((100, 100), pg.SRCALPHA)
S1.fill((255, 0, 0))

S2 = pg.Surface((100, 100), pg.SRCALPHA)
S2.fill((255, 255, 0))

A = AnimationSet.new(S1, 10)
A.add(1, [S2], 1)

print(A)
i = 0
state = 0


while win.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            win.running = False
            

    # start of the game loop
    win.heading()


    # game logic here
    win.loop()
    i += 1
    if (i%120 == 0): 
        state = 1 if state == 0 else 0
        A.update(state=state)
    win.blit(A, (1, 1, 10, 10), state=state)

    # end of the game loop
    win.tailing()


