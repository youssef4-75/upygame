import pygame 


class Window:
    def __init__(self, title: str, width: int, height: int):
        self.title = title
        self.width = width
        self.height = height

    def show(self):
        print(f"Showing window '{self.title}' with size {self.width}x{self.height}.")

    def close(self):
        print(f"Closing window '{self.title}'.")