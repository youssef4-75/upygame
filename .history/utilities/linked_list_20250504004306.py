


class LinkedList:
    def __init__(self, value):
        self.__value = value
        self.__next = None 

    @property 
    def value(self):
        return self.__value
    
    def link(self, other):
        