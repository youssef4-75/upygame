

class Peace:
    def __init__(self, row: int, column: int, side, valid_moves: Iterable[tuple]):
        self.__pos = [row, column]
        self.__side = side

    @property
    def side(self):
        return self.__side 
    
    @property
    def x(self):
        return self.__pos[0]

    @property
    def y(self):
        return self.__pos[1]
    

    


    