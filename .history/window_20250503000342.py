import pygame as pg




class Window:
    def __init__(self, title: str, width: int, height: int, *phases: function):
        self.title = title
        self.width = width
        self.height = height

        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        
        self.running = True

        self.phase = 0
        self.phases = phases
    
    def get_screen(self):
        return self.screen
    
    def white(self):
        return self.fill((255, 255, 255))
    
    def blit(self, screen: pg.Surface, pos: tuple):
        self.screen.blit(screen, pos)

    def fill(self, color: tuple):
        self.screen.fill(color)

    def update(self):
        pg.display.update()

    def tick(self, fps: int):
        self.clock.tick(fps)

    def quit(self):
        pg.quit()

    def tailing(self):
        self.update()
        self.tick(60)

    def heading(self):
        self.white()

    def loop(self, *args, ):
        ...


    
    