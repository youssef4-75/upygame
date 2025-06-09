from typing import Iterable
from pygame import Surface, SRCALPHA
from multipledispatch import dispatch

from .animation import Animation


class AnimationSet:
    def __init__(self, animations: dict[int, Animation], 
                priorities: dict[int, int], frame_speed) -> None:
        # keys are numbers
        # create priority when you make a new gif collection + 
        # modify classmethod to be convenient 
        assert len(animations) == len(priorities)
        self.__animations = animations
        self.__priorities = priorities
        if animations:self.__state = next(iter(animations))
        else: self.__state = None
        self.__wait = None
        self.__frame_speed = frame_speed
        self.__reset = False
    
    def __str__(self) -> str:
        p = f"""{self.__class__.__name__}: <{}
        for key, animation in self.__animations.items():
            p += f"\n\t{key} : {animation}, {self.__priorities[key]}"
        return p + "\n>"""

    @classmethod
    def new(cls, surf: Surface, frame_speed: int):
        """
        create a new AnimationSet with a single animation,
        the animation is a single frame animation, with the key 0 and the priority 1
        
        the frame speed is the speed of the animation
        """
        return cls({0: Animation([surf])}, {0: 1}, frame_speed)

    def add_sample_color(
                self, 
                key: int, 
                color: tuple[int, int, int],
                size: tuple[int, int]=(100, 100), 
                priority: int=1) -> None:
        
        transparent_surface = Surface(size, SRCALPHA)
        transparent_surface.fill(color)
        self.add(key, Animation([transparent_surface]), priority)

    def add(self,
            key: int, 
            animation: Animation|Iterable[Surface], 
            priority: int):
        """
        add an animation to the collection, if the key is already 
        in the collection, add the given frames to the previous one
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

    def get_animation(self):
        if self.__state is None: return None
        try:return self.__animations[self.__state]
        except KeyError:
            return None
    
    def get_priority(self, index=None):
        if index is None: index = self.__state
        return self.__priorities[index]
    
    def compare_priority(self, anim_index1, anim_index2):
        if anim_index1 == anim_index2: return False
        return self.get_priority(anim_index1) <= self.get_priority(anim_index2)

    def decide(self, state=None, start=None, repeat=None):
        """
        decide the next surface to plot following these rules: 
            if the current animation have a priority higher than the priority of the 
                    suggested one, it wait until the end of the current animation
            otherwise, it is switched
            if state is None: return the next frame of the current animation
        """
        if state is None or state not in self.__animations:
            state = self.__state
            print("AnimationSet: state is None or not in animations, using current state")
        animation = self.get_animation()
        if animation is None: return None
        if self.__reset: animation.reset()
        animation.update(start, repeat)
        self.__reset = False
        self.__wait = state
        if self.compare_priority(self.__state, self.__wait) or animation.ended:
            # we cant switch animation unless the current one is finished or the suggested one is an emergency one
            self.__state = self.__wait
            self.__wait = None
            if self.__state != self.__wait: self.__reset = True
            
        return animation.generate(self.__frame_speed)
    
    def convert_alpha(self):
        for gif in self.__animations.values(): 
            gif.convert_alpha()

            