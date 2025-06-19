"""
Animation module for handling sprite animations in Pygame.

This module provides the Animation class which manages sequences of Pygame surfaces
to create frame-based animations. It supports features like frame rate control,
looping, and frame manipulation.
"""

from pygame import Surface
from typing import Iterable
from os import listdir
from os.path import isfile, join, isabs, abspath
from pygame.image import load as pg_load
from pygame.transform import scale as pg_scale

from ..utilities.utilities import loop_method, init_method

RATIO = 100  # ratio to convert from fps to mfps or any fraction of fps


class Animation:
    """
    A class to manage and control frame-based animations using Pygame surfaces.
    
    This class handles the sequencing and timing of animation frames, supporting
    features like frame rate control, looping, and frame manipulation. It's designed
    to work seamlessly with Pygame's Surface objects.
    
    Attributes:
        SL (tuple[Surface]): Sequence of surfaces representing animation frames
        __start (int): Starting frame index for the animation
        __current (int): Current frame index
        __repeat (int): End frame index for the animation
    """
    
    def __init__(self, Content_list: Iterable[Surface]) -> None:
        """
        Initialize an Animation object with a sequence of surfaces.
        
        Args:
            Content_list (Iterable[Surface]): A sequence of Pygame surfaces or a single surface
                to create the animation frames.
        
        Raises:
            TypeError: If Content_list is neither a Surface nor an iterable of Surfaces
        """
        if isinstance(Content_list, Iterable): self.SL = tuple(Content_list)
        elif isinstance(Content_list, Surface): self.SL = (Content_list, )
        else: raise TypeError("""The content of an animation must be a
pygame surface or a list-like of pygame surfaces""")
        
        self.__start = 0  # mark the start of the animation, usefull for 
                            # special animations where each time you loop you 
                            # start from a different point.
                            # 1 2 3 4 5 6 7 3 4 5 6 7 3 4 ...
        self.__current = 0  # mark the current frame index
        self.__repeat = len(Content_list)  # mark the end frame of the animation
    
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

    @property
    def start(self):
        return RATIO *self.__start
    
    @property
    def repeat(self):
        return RATIO * self.__repeat
   
    @init_method
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
    def ended(self) -> bool:
        """
        Check if the animation has reached its end.
        
        Returns:
            bool: True if the animation has ended, False otherwise
        """
        return self.__current >= self.repeat
    
    @property
    def current_frame(self) -> Surface:
        """
        Get the current frame of the animation.
        
        Returns:
            Surface: The current Pygame surface being displayed
        """
        return self.SL[int(self.__current // RATIO)]

    @loop_method
    def generate(self, frame_speed: int) -> Surface:
        """
        Generate the next frame of the animation.
        
        Args:
            frame_speed (int): The speed at which to advance the animation
            
        Returns:
            Surface: The next frame to display
        """
        Surf = self.current_frame 
        self.__current = self.__current + frame_speed
        if self.ended:
            self.__current = self.start
        return Surf
        
    @loop_method
    def update(self, start: int = None, repeat: int = None) -> None:
        """
        Update the animation's start and end points.
        
        Args:
            start (int, optional): New starting frame index
            repeat (int, optional): New end frame index
        """
        if start: self.__start = start
        if repeat:self.__repeat = min(repeat, len(self.SL))
    
    @loop_method
    def reset(self) -> None:
        """
        Reset the animation to its initial state.
        Sets start and current frame to 0 and repeat to the total frame count.
        """
        self.__start = self.__current = 0
        self.__repeat = len(self.SL)

    def convert_alpha(self) -> None:
        """
        Convert all frames to use alpha channel for transparency.
        This is useful for sprites with transparent backgrounds.
        """
        for i, S in enumerate(self.SL):
            self.SL[i] = S.convert_alpha()
        self.SL = tuple(self.SL)
    
    @init_method
    def add_frames(self, *frames: Iterable[Surface]) -> None:
        """
        Add new frames to the animation.
        
        Args:
            *frames (Iterable[Surface]): Variable number of surfaces to add as frames
        """
        for frame in frames:
            self.SL += (frame, )
        self.__repeat = len(self.SL) 

