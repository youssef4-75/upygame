from typing import Callable


class Card:
    """
    TODO: this class represents the cards in board games, each card have an effect ...
    """
    def __init__(self, effect: Callable):
        self.__effect = effect

    
