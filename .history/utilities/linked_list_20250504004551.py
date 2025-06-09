


class LinkedList:
    def __init__(self):
        self.__value = ...
        self.__next = None 

    @property 
    def value(self):
        return self.__value
    
    @value.setter

    
    def link(self, other):
        if self.__next is None: self.__next = other 

    def __getitem__(self, slice):
        result = self.__next
        for i in range(slice):
            