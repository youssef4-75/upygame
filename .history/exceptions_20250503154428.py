

class MaximumCallsReachedError(Exception):
    """Exception raised when the maximum number of calls is reached."""

    def __init__(self, number: int):
        self.message = f"Maximum number of calls reached: {number}."
        super().__init__(self.message)

