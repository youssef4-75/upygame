import pygame as pg 
from window import Window
from loops import loop1

win = Window("Test", 800, 600, )
win.white()
win.add_

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


