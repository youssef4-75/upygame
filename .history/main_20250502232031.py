import pygame as pg 


def run(title, width, height, background=Nnoe):
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    
    clock = pg.time.Clock()