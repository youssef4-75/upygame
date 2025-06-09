from pygame import Surface

from .frame import Animation


class GifCollection[Content]:
    def __init__(self, animations: dict[int, Animation[Content]], 
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
        p = "GIF_Collection: <"
        for key, animation in self.__animations.items():
            p += f"\n\t{key} : {animation}, {self.__priorities[key]}"
        return p + "\n>"

    @classmethod
    def new(cls, frame_speed):
        return cls({}, {}, frame_speed)
    
    def add_sample_color(self, color: tuple[int, int, int]):
        surf = Surface
    
    def add(self, key: int, Gif: Animation[Content], priority: int):
        if not self.__animations: self.__state = key
        self.__animations[key] = Gif; self.__priorities[key] = priority
    
    def get_animation(self):
        return self.__animations[self.__state]
    
    def get_priority(self, index=None):
        if index is None: index = self.__state
        return self.__priorities[index]
    
    def compare_priority(self, anim_index1, anim_index2):
        if anim_index1 == anim_index2: return False
        return self.get_priority(anim_index1) <= self.get_priority(anim_index2)

    def decide(self, state, start=None, repeat=None):
        """
        decide the next surface to plot following these rules: 
            if the current animation have a priority higher than the priority of the 
                    suggested one, it wait until the end of the current animation
            otherwise, it is switched
            if state is None: return the next frame of the current animation


        """
        animation = self.get_animation()
        if self.__reset: animation.reset()
        animation.update(start, repeat)
        self.__reset = False
        self.__wait = state
        if self.compare_priority(self.__state, self.__wait) or animation.full:
            self.__state = self.__wait
            self.__wait = None
            if self.__state != self.__wait: self.__reset = True
            
        return animation.generate(self.__frame_speed)
    
    def convert_alpha(self):
        for gif in self.__animations.values(): 
            gif.convert_alpha()

            