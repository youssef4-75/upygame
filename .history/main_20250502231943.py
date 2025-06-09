import pygame as pg 


def run(width, height):
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("War Zone")
    surface = pg.image.load("assets/background.jpg").convert()
    clock = pg.time.Clock()