from pygame import Surface
from typing import Iterable
from os import listdir
from os.path import isfile, join, isabs, abspath
from pygame.image import load as pg_load
from pygame.transform import scale as pg_scale


RATIO = 100  # ratio to convert from fps to mfps or any fraction of fps


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
        self.__repeat = RATIO * (len(Content_list) - 1)  # mark the end frame of the animation
    
    def __len__(self):return len(self.SL)

    def __str__(self) -> str:
        return f"<Animation({len(self)}, current={self.__current//RATIO})>"

    def __add__(self, other):
        if isinstance(other, Surface): 
            self.add_frames(other)
            return self 
        if isinstance(other, Animation): 
            return Animation(list(other.SL) + list(self.SL))
        if isinstance(other, Iterable): 
            self.add_frames(*other)
            return self
        raise TypeError("Animation.__add__: other must be a Surface, Surface list or an Animation")

    @classmethod
    def from_directory(cls, directory: str, size: tuple = None, *args, **kwargs):
        """
        create an animation from a directory of images
        images in the directory are ordered by name
        """
        
        if not isabs(directory): directory = abspath(directory)
        files: list[str] = [f for f in listdir(directory) if isfile(join(directory, f))]
        files.sort()
        
        frames = []
        for file in files:
            frame = pg_load(join(directory, file))
            if size or args or kwargs: frame = pg_scale(frame, size, *args, **kwargs)
            frames.append(frame)
        
        return cls(frames)
    
    @property
    def ended(self):
        """whether the animation has ended or not yet"""
        return self.__current >= self.__repeat + RATIO
    
    @property
    def current_frame(self):
        return self.SL[int(self.__current // RATIO)]

    def generate(self, frame_speed):
        # frame speed in .01fps
        Surf = self.current_frame 
        self.__current = self.__current + frame_speed
        if self.__current > self.__repeat + RATIO:
            self.__current = self.__start
        return Surf
        
    def update(self, start=None, repeat=None):
        if start: self.__start = start
        if repeat:self.__repeat = min(repeat, len(self.SL) - 1)
    
    def reset(self):
        self.__start = self.__current = 0
        self.__repeat = RATIO * (len(self.SL) - 1)

    def convert_alpha(self):
        for i, S in enumerate(self.SL):
            self.SL[i] = S.convert_alpha()
        self.SL = tuple(self.SL)
    
    def add_frames(self, *frames: Iterable[Surface]):
        for frame in frames:
            self.SL += (frame, )
        self.__repeat = RATIO * (len(self.SL) - 1)