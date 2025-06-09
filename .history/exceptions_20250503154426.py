

class MaximumCallsReachedError(Exception):
    """Exception raised when the maximum number of calls is reached."""

    def __init__(self, number: int):
        self.message = f""
        super().__init__(self.message)

