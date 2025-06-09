# Upygame

A powerful extension library for Pygame that provides enhanced functionality for game development.

## Features

### Animation System

- **Animation and AnimationSet (AnSet) Classes**
  - Create single animations
  - Create animation sets
  - Add frames to animations
  - Add frames or animations to an AnSet (either to existing animations or as new ones)
  - Retrieve surfaces for rendering
  - Define frame rates per AnSet
  - Control animation start/end points
  - Switch between animations within an AnSet

### Interaction Management

- **Efficient Object Interaction System**
  - Optimized algorithms for handling multiple object interactions
  - Reduced complexity for interaction-based games
  - Enhanced performance for games with many interactive elements

### Board Game Framework

- **Comprehensive Board Game Tools**
  - Grid-based position management
  - Turn management system
  - Valid move validation
  - User input handling (mouse clicks, drag-and-drop)
  - Efficient UI rendering
  - Turn indicators and move highlighting
  - Smooth move animations
  - Debugging utilities

### Additional Features

- **Online Game Scaling Support**

  - Tools and utilities for scaling games to online platforms

- **Method Usage Limiter**

  - Decorator to restrict method calls per instance
  - Prevents accidental method placement in game loops

- **Window Management**
  - Enhanced Window class with Surface compatibility
  - Seamless integration with:
    - AnimationSet and Animation classes
    - Board game framework

This is a modified version for pygame, where I created Alhamdulilah things I feel needing everytime I used pygame.

features included: - a class to handle interaction between objects that are two many, implementing some algorithm to reduce the interaction complexity, and enhance the games that are based on interaction. - a class to handle board games, with all tools needed to implement one.
you can:
_ get the postition of a cell in the grid ෴
_ manage turn in an effecient way
_ check valid moves for pieces ෴
_ receiving user input (mouse click, drag-n-drop, ...) ෴
_ drawing the UI element without conumming process time
_ show the turn indicators, and the possible moves for each piece
_ animate the moves smoothly
_ effecient tools for debugging the game

    - a class to facilitate scaling to be an online game.
    - a decorator to force using a method for a limited number of times per instance, to prevent putting methods in the game loop by accident
    - a Window class to facilitate creating the game window, and creating objects in it, can be treated as a Surface object though, it is compatible with :
        * AnSet, Animation
        * Board

### Note

I made some changes in the source files for the dispatch function to let it accept an Ellipsis object to define a default function, these changes are:


adding these lines:
    if len(types) >= 1 and types[0] == Ellipsis: 
        types = (type(...), )
    types = tuple(types)
in the beggining of the dispatch function


rewrote the function dispatch in the Dispatcher class

def dispatch(self, *types):
    """Deterimine appropriate implementation for this type signature

    This method is internal.  Users should call this object as a function.
    Implementation resolution occurs within the ``__call__`` method.

    >>> from multipledispatch import dispatch
    >>> @dispatch(int)
    ... def inc(x):
    ...     return x + 1

    >>> implementation = inc.dispatch(int)
    >>> implementation(3)
    4

    >>> print(inc.dispatch(float))
    None

    See Also:
        ``multipledispatch.conflict`` - module to determine resolution order
    """
    # print(types, self.funcs.keys())
    if types in self.funcs:
        return self.funcs[types]
    try:
        return next(self.dispatch_iter(*types))
    
    except StopIteration:
        if (type(...), ) in self.funcs:
            return self.funcs[(type(...), )]
        return None


to test, you may run: 

from multipledispatch import dispatch


@dispatch(int, int)
def f(a: int, b: int): 
    return a-b


@dispatch(str, str)
def f(a: str, b: str): 
    return a+b


@dispatch(...)
def f(a, b):
    return a

print(f(3, 2))
print(f("3", "2"))
print(f(["3", "2"], 9))

