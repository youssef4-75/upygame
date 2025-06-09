from 


class GifCollection[Content]:
    def __init__(self, gifs: dict[int, Animation[Content]], priorities: dict[int, int], frame_speed) -> None:
        # keys are numbers
        # create priority when you make a new gif collection + modify classmethod to be convenient 
        assert len(gifs) == len(priorities)
        self.__gifs = gifs
        self.__priorities = priorities
        if gifs:self.__state = next(iter(gifs))
        else: self.__state = None
        self.__wait = None
        self.__frame_speed = frame_speed
        self.__reset = False
    
    def __str__(self) -> str:
        p = "GIF_Collection: <"
        for key, gif in self.__gifs.items():
            p += f"\n\t{key} : {gif}, {self.__priorities[key]}"
        return p + "\n>"

    @classmethod
    def new(cls, frame_speed):
        return cls({}, {}, frame_speed)
    
    def add(self, key: int, Gif: Animation[Content], priority: int):
        if not self.__gifs: self.__state = key
        self.__gifs[key] = Gif; self.__priorities[key] = priority
    
    def get_gif(self):
        return self.__gifs[self.__state]
    
    def get_priority(self, index=None):
        if index is None: index = self.__state
        return self.__priorities[index]
    
    def compare_priority(self, gif_index1, gif_index2):
        if gif_index1 == gif_index2: return False
        return self.get_priority(gif_index1) <= self.get_priority(gif_index2)

    def decide(self, state, start=None, repeat=None):
        self.__state == 5
        # if x: ic(str(self), self.get_priority(1), self.get_priority(5), )
        gif = self.get_gif()
        if self.__reset: gif.reset()
        gif.update(start, repeat)
        self.__reset = False
        self.__wait = state
        if self.compare_priority(self.__state, self.__wait) or gif.full:
            self.__state = self.__wait
            self.__wait = None
            if self.__state != self.__wait: self.__reset = True
        return gif.generate(self.__frame_speed)
    
    def convert_alpha(self):
        for gif in self.__gifs.values(): 
            gif.convert_alpha()

            