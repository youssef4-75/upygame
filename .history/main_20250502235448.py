import pygame as pg 
from window import Window

win = Window("Test", 800, 600)
win.white()

while win.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            win.running = False
            
    win.fill((255, 255, 255))
    win.update()
    win.tick(60)

