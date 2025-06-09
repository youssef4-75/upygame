

class MaximumCallsReachedError(Exception):
    """Exception raised when the maximum number of calls is reached."""

    def __init__(self, number: int, method_name: str):
        
        super().__init__(f"Maximum number of calls ({number}) for {method_name}"
            +" reached, can't call it anymore")

class SideAlreadySetError(Exception):
    def __init__(self, side, sides):
        super().__init__(f"the player with the number {side} already exist, "
            +"so do the {sides} players")

class MoveCollisionError(Exception): 
    def __init__(self, peace):
        super().__init__(f"the peace {peace} haven't announced an end for "
            +"its activity yet, end it first before moving to the new peace")