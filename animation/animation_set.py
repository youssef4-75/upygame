"""
AnimationSet module for managing multiple animations with priority-based transitions.

This module provides the AnimationSet class which manages collections of animations
with priority-based switching between different animation states. It's useful for
complex game entities that need to handle multiple animation states (like idle,
walking, jumping, etc.) with smooth transitions between them.
"""

from typing import Iterable
from pygame import Surface, SRCALPHA
from os import listdir
from os.path import isfile, join, abspath, isabs

from ..utilities.utilities import loop_method, init_method

from .animation import Animation


class AnimationSet:
    """
    A class to manage multiple animations with priority-based transitions.
    
    This class handles collections of animations that can be switched between based
    on priority levels. It's particularly useful for game entities that need to
    handle multiple animation states (idle, walking, jumping, etc.) with smooth
    transitions between them.
    
    Attributes:
        __animations (dict[int, Animation]): Dictionary mapping state keys to animations
        __priorities (dict[int, int]): Dictionary mapping state keys to priority levels
        __state (int): Current animation state
        __wait (int): Next animation state to transition to
        __frame_speed (int): Base frame speed for all animations
        __reset (bool): Flag indicating if animation should reset
    """
    
    def __init__(self, animations: dict[int, Animation], 
                priorities: dict[int, int], frame_speed: int) -> None:
        """
        Initialize an AnimationSet with a collection of animations.
        
        Args:
            animations (dict[int, Animation]): Dictionary of animations indexed by state keys
            priorities (dict[int, int]): Dictionary of priority levels for each state
            frame_speed (int): Base frame speed for all animations
            
        Note:
            The length of animations and priorities must match
        """
        assert len(animations) == len(priorities)
        self.__animations = animations
        self.__priorities = priorities
        if animations:self.__state = next(iter(animations))
        else: self.__state = None
        self.__wait = None
        self.__frame_speed = frame_speed
        self.__reset = False
    
    def __str__(self) -> str:
        p = f"{self.__class__.__name__}<"
        for key, animation in self.__animations.items():
            p += f"\n\t{key} : {animation}, priority={self.__priorities[key]}"
        return p + "\n>"

    @classmethod
    def new(cls, anim: Surface|Iterable[Surface]|Animation, frame_speed: int) -> 'AnimationSet':
        """
        Create a new AnimationSet with a single animation.
        
        Args:
            anim (Surface|Iterable[Surface]|Animation): The initial animation
            frame_speed (int): Base frame speed for the animation
            
        Returns:
            AnimationSet: A new AnimationSet instance with a single animation
        """
        if isinstance(anim, Surface): anim = Animation([anim])
        if isinstance(anim, Iterable): anim = Animation(anim)
        return cls({0: anim}, {0: 1}, frame_speed)

    @init_method
    def add_sample_color(self, 
                key: int, 
                color: tuple[int, int, int],
                size: tuple[int, int]=(100, 100), 
                priority: int=1) -> None:
        """
        Add a solid color animation to the set.
        
        Args:
            key (int): State key for the new animation
            color (tuple[int, int, int]): RGB color values
            size (tuple[int, int], optional): Size of the color surface. Defaults to (100, 100)
            priority (int, optional): Priority level. Defaults to 1
        """
        transparent_surface = Surface(size, SRCALPHA)
        transparent_surface.fill(color)
        self.add(key, Animation([transparent_surface]), priority)

    @init_method
    def add(self,
            key: int, 
            animation: Animation|Iterable[Surface], 
            priority: int) -> None:
        """
        Add an animation to the set or append frames to an existing animation.
        
        Args:
            key (int): State key for the animation
            animation (Animation|Iterable[Surface]): Animation to add
            priority (int): Priority level for the animation
        """
        if key in self.__animations:
            if isinstance(animation, Animation): 
                self.__animations[key].add_frames(*animation.SL)
            elif isinstance(animation, Iterable):
                self.__animations[key].add_frames(*animation)
            else: raise TypeError("AnimationSet.add: animation must be an Animation or an iterable of Surfaces")
            return 
        if not isinstance(animation, Animation):
            if isinstance(animation, Iterable): animation = Animation(animation)
            else: raise TypeError("AnimationSet.add: animation must be an Animation or an iterable of Surfaces")
        if not self.__animations: self.__state = key  # if the collection is empty, set the state to the new key
        self.__animations[key] = animation; self.__priorities[key] = priority
    
    @init_method
    @classmethod
    def from_directory(cls, frame_speed, directory: str, size: tuple=None, separator: str="x"):
        """
        directory: is a path for a directory containing other directories
            each subdirectory is transformed into an animation
            the subdirectory name is in the form key{separator}priority
            the key and priority are separated by the separator
        """

        animation = {}
        priorities = {}
        if not isabs(directory): directory = abspath(directory)
        for d in listdir(directory):
            if isfile(join(directory, d)):
                continue
            
            try: key, priority = map(int, d.split(separator))
            except ValueError:
                print(f"AnimationSet.get_from_directory: {d} is not a valid directory name, skipping")
                continue
            path = f"{directory}/{d}"
            animation[key] = Animation.from_directory(path, size)
            priorities[key] = priority
        return cls(animation, priorities, frame_speed)

    @property
    def get_animation(self) -> Animation | None:
        """
        Get the current animation.
        
        Returns:
            Animation | None: The current animation or None if not initialized
        """
        if self.__state is None: return None
        try:return self.__animations[self.__state]
        except KeyError:
            return None
    
    def get_priority(self, index: int = None) -> int | None:
        """
        Get the priority level for an animation state.
        
        Args:
            index (int, optional): State key to get priority for. Defaults to current state
            
        Returns:
            int | None: Priority level or None if state doesn't exist
        """
        if index is None: index = self.__state
        try:return self.__priorities[index]
        except KeyError:
            return None
    
    def __compare_priority(self, anim_index1, anim_index2):
        """
        if its the same index: return False
        if they are different index: return first index 
            priority is less than or equal to the second ones'

        used to define whether to stop the current animation 
            and switch to another one or just keep with the 
            current untill it ends 
        """
        if anim_index1 == anim_index2: return False
        return self.get_priority(anim_index1) <= self.get_priority(anim_index2)

    @loop_method
    def generate(self, state: int = None, start: int = None, repeat: int = None) -> Surface | None:
        """
        Generate the next frame based on current state and priorities.
        
        Args:
            state (int, optional): Suggested next state
            start (int, optional): Starting frame for current animation
            repeat (int, optional): End frame for current animation
            
        Returns:
            Surface | None: Next frame to display or None if no animation available
        """
        
        if state is None or state not in self.__animations:
            state = self.__state
            print("AnimationSet: state is None or not in animations, using current state")
        animation = self.get_animation  # get the current animation
        
        if animation is None: return None
                
        animation.update(start, repeat)
        self.__reset = False
        self.__wait = state
        if self.__compare_priority(self.__state, self.__wait) or animation.ended:
            # we cant switch animation unless the current one is finished or the suggested one is an emergency one
            self.__state = self.__wait
            self.__wait = None
            self.__reset = True

        if self.__reset: 
            animation.reset()
            
        return animation.generate(self.__frame_speed)
    
    def convert_alpha(self):
        for anim in self.__animations.values(): 
            anim.convert_alpha()

            