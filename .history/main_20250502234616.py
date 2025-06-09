import pygame as pg 


def run(title, width, height):
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    pg.time.Clock()
    return screen