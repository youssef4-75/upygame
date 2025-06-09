

class Peace:
    def __init__(self, row: int, column: int, side):
        self.__pos = [row, column]
        self.__side = side

    @property
    def side(self):
        return self.__side 
    



    