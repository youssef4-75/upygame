


class LinkedList:
    def __init__(self, value):
        self.__value = value
        self.__next = None 

    @property 
    def value(self):
        return self.__value
    
    def link(self, other):
        if self.__next is None: self.__next = other 

    def __getitem__(self, slice):
        for i in range()