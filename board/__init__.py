"""
Board game module for creating and managing grid-based games.

This module provides a framework for creating grid-based board games with the following components:

- Board: A grid-based game board that manages pieces, player turns, and game phases
- Piece: Abstract base class for game pieces with position and side management
- Phase: Game phase management with event-driven logic and conditions
- Card: Class for managing game cards with flexible attributes and effects
- Deck: Class for managing collections of cards with drawing and shuffling operations

The module supports features like:
- Grid-based board management
- Piece movement and interaction
- Player turns and sides
- Game phases with conditions and effects
- Event-driven game logic
- Mouse and keyboard input handling
- Card and deck management
- Visual representation of game elements
"""

from .board import Board
from .piece import Piece
from .phase import Phase
from .card import Card, CardVisuals
from .deck import Deck
from .var import Column_X, Row_Y
from .exception import FinalRepException

__all__ = [
    'Board',
    'Piece',
    'Phase',
    'Card',
    'CardVisuals',
    'Deck',
    'Column_X',
    'Row_Y',
    'FinalRepException'
]
