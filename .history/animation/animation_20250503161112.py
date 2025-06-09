from pygame import Surface
from typing import Iterable

from utilities import limit_calls


class Animation:
    def __init__(self, Content_list: Iterable[Surface]) -> None:
        if isinstance(Content_list, Iterable): self.SL = tuple(Content_list)
        elif isinstance(Content_list, Surface): self.SL = (Content_list, )
        else: raise TypeError("""The content of an animation must be a
pygame surface or a list-like of pygame surfaces""")
        
        self.__start = 0  # mark the start of the animation, usefull for 
                            # special animations where each time you loop you 
                            # start from a different point.
                            # 1 2 3 4 5 6 7 3 4 5 6 7 3 4 ...
        self.__current = 0  # mark the current frame index
        self.__repeat = len(Content_list) - 1  # mark the end frame of the animation
    
    def __len__(self):return len(self.SL)

    def __str__(self) -> str:
        return f"<Animation({len(self)}, current={self.__current})>"

    def __radd__(self, other: Surface):
        print("radd")
        
    def __add__(self, other):
        return Animation(list(other.SL) + list(self.SL))

    def generate(self, frame_speed):
        Surf = self.SL[int(self.__current)]
        self.__current = int(self.__current + frame_speed)
        if self.__current > self.__repeat: 
            self.__current = self.__start
        return Surf

    @property
    def ended(self):
        return self.__current >= self.__repeat
        
    def update(self, start=None, repeat=None):
        if start:self.__start = start
        if repeat:self.__repeat = min(repeat, len(self.SL) - 1)
    
    def reset(self):
        self.__start = self.__current = 0
        self.__repeat = len(self.SL) - 1

    def convert_alpha(self):
        for i, S in enumerate(self.SL):
            self.SL[i] = S.convert_alpha()
        self.SL = tuple(self.SL)

    @limit_calls(1)
    def add_frames(self, *frames: Iterable[Surface]):
        for frame in frames:
            self.SL += (frame, )
        self.__repeat = len(self.SL) - 1