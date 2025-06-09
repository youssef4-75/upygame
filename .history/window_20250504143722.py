import pygame as pg
from multipledispatch import dispatch
from animation import AnimationSet
from board import Board



class Window:
    def __init__(self, title: str, width: int, height: int, *phases):
        self.title = title
        self.width = width
        self.height = height

        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        
        self.running = True

        self.phase = 0
        self.phases = phases or [lambda *a, **k: None]
    
    def __getattribute__(self, name):
        try:
            # Get the attribute normally
            attr = super().__getattribute__(name)
            
            return attr
        
        except AttributeError:
            try: 
                attr = getattr(self.screen, name)
                return attr 
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def get_screen(self):
        return self.screen
    
    def add_params(self, **kwargs):
        self.new_param = kwargs

    def white(self):
        return self.fill((255, 255, 255))
    
    @dispatch(pg.Surface, object)
    def blit(self, surface: pg.Surface, pos: tuple):
        self.screen.blit(surface, pos)
    
    @dispatch(AnimationSet, object)
    def blit(self, surface: AnimationSet, pos: tuple|pg.Rect, *, state=None):
        self.screen.blit(surface.generate(state), pos)   

    @dispatch(Board)
    def blit(self, surface: Board, *, state=None):
        for i in range(suf)
        

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

    def loop(self, *args, **kwargs):
        self.phases[self.phase](self, *args, **kwargs, **self.new_param)


    
    