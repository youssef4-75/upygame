


class FinalRepException(BaseException):
    def __init__(self, phase) -> None:
        return super().__init__(f"""Private Exception: This
phase with id = {id(phase)} cannot be repeated anymore""")