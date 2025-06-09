import pygame as pg


class Window:
    def __init__(self, title: str, width: int, height: int):
        self.title = title
        self.width = width
        self.height = height

        self.__screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        pg.time.Clock()
        return screen

    