import pygame as pg


class Window:
    def __init__(self, title: str, width: int, height: int):
        self.title = title
        self.width = width
        self.height = height

        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        
        self.running = True
    
    def update(self):
        pg.display.update()

    def tick(self, fps: int):
        self.clock.tick(fps)

    def quit(self):
        pg.quit()

    