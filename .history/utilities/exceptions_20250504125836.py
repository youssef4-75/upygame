

class MaximumCallsReachedError(Exception):
    """Exception raised when the maximum number of calls is reached."""

    def __init__(self, number: int, method_name: str):
        self.message = f"Maximum number of calls ({number}) for {method_name} reached, can't call it anymore"
        super().__init__(self.message)

class Re