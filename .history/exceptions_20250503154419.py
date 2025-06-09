

class MaximumCallsReachedError(Exception):
    """Exception raised when the maximum number of calls is reached."""

    def __init__(self, number: int, message="Maximum number of calls reached."):
        self.message = message
        super().__init__(self.message)

