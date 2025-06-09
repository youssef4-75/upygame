import pygame as pg 


def run(WIDTH, HEIGHT):
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("War Zone")
    surface = pg.image.load("assets/background.jpg").convert()
    clock = pg.time.Clock()