from typing import Callable, Any
import pygame as pg
from multipledispatch import dispatch

from .animation import AnimationSet
from .board import Board, Phase



class Window:
    def __init__(self, title: str, width: int, height: int, *loop_phases: Callable, with_layers=False):
        self.title = title
        self.width = width
        self.height = height

        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        
        self.running = True

        self.new_param = {}
        self.loop_phases = loop_phases or [lambda *a, **k: ...]
        self.white()
        self.key_map = {}
        if with_layers: self.init_layers()
    
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
    
    def init_layers(self):
        self.layers: dict[Any, pg.Surface] = {}

    def add_layer(self, key):
        self.layers[key] = pg.Surface((self.width, self.height), flags=pg.SRCALPHA)
        self.layers[key].fill((0, 0, 0, 0))

    def get_screen(self):
        return self.screen
    
    def add_params(self, *_, **kwargs):
        self.new_param.update(kwargs)

    def white(self):
        return self.fill((255, 255, 255))
    
    def add_loop_phase(self, lphase: Callable):
        self.loop_phases.append(lphase)
    
    @dispatch(...)
    def blit(self, any: Any, *args, **kwargs):
        try: 
            any.__blit__(*args, **kwargs)
        except AttributeError as e: 
            print(e)

    @dispatch(pg.Surface, object)
    def blit(self, surface: pg.Surface, pos: tuple):
        self.screen.blit(surface, pos)
    
    @dispatch(AnimationSet, object)
    def blit(self, surface: AnimationSet, pos: tuple|pg.Rect, *, state=None):
        self.screen.blit(surface.generate(state), pos)   

    @dispatch(Board)
    def blit(self, surface: Board, *,
            limits: bool = False, color=(0, 0, 0),
            line_width=2, overflow: bool = True):
        
        for i in range(surface.row):
            for j in range(surface.column):
                rect, color_ = surface.get_cell(i, j)
                surf = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
                surf.fill(color_)
                self.screen.blit(surf, rect)
        
        for piece in surface.pieces:
            surface.draw_piece(self, piece, overflow=overflow)

        if not limits: return

        for i in range(surface.row + 1):
            level = surface.top + i*surface.cell_height
            pg.draw.line(self.screen, color, 
                    (surface.left, level),
                    (surface.right, level),
                    line_width)
        
        for j in range(surface.column + 1):
            level = surface.left + j*surface.cell_width
            pg.draw.line(self.screen, color, 
                    (level, surface.top),
                    (level, surface.bottom), 
                    line_width)

    def fill(self, color: tuple):
        self.screen.fill(color)

    def update(self):
        pg.display.update()

    def tick(self, fps: int):
        self.clock.tick(fps)

    def quit(self):
        pg.quit()

    def tailing(self):
        for layer in self.layers.values():
            self.screen.blit(layer, (0, 0, self.width, self.height))
        self.update()
        self.tick(60)

    def heading(self):
        self.white()

    def loop(self, *args, **kwargs):
        self.listen(*args, **kwargs)
        for step in self.loop_phases:
            step(*args, **kwargs, **self.new_param)

    def add_key_map(self, key: int, func: Callable, *, once: bool = False):
        """
        a function to add an event listener in the game, if the key is pressed, 
        then the funcfunction is called, once define whether to wait until you 
        stop pressing the button to activate the function another time or to 
        keep activating the funct as long as you still press it
        """
        self.key_map[key] = [func, False, once]

    def listen(self, *args, **kwargs): 
        # once: determine if you pressed the key two successive times, would you recall the function or wait untill the press is done
        keys = pg.key.get_pressed()
        for key, (func, being_called, once) in self.key_map.items():
           
            if keys[key]:
                if not once:
                    func(*args, **kwargs); continue
                if not being_called:
                    func(*args, **kwargs);
                    self.key_map[key][1] = True;
            else:
                self.key_map[key][1] = False

