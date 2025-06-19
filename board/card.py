"""
Card module for managing game cards with flexible attributes and effects.

This module provides the Card class which represents cards in board games with
support for visual representation, activation effects, and customizable attributes.
"""

from typing import Callable, Optional, Any, Dict
import pygame as pg
from pygame import Surface, Rect, SRCALPHA
from dataclasses import dataclass

@dataclass
class CardVisuals:
    """Data class for card visual properties"""
    surface: Surface
    rect: Rect
    scale: float = 1.0
    rotation: float = 0.0
    alpha: int = 255

class Card:
    """
    A class to represent cards in board games with flexible attributes and effects.
    
    This class handles card properties, visual representation, activation effects,
    and ownership management. It's designed to be adaptable to various game mechanics
    through customizable attributes.
    
    Attributes:
        __effect (Callable): The effect function to be executed when card is activated
        __owner (Any): The current owner of the card
        __visuals (Optional[CardVisuals]): Visual properties if representation is enabled
        __attributes (Dict[str, Any]): Custom attributes for specific game mechanics
        __name (str): The name of the card
        __description (str): The description of the card
        __image_path (str): Path to the card's image file
    """
    
    def __init__(self, name: str, description: str, image_path: str, effect: Callable, **new_params) -> None:
        """
        Initialize a Card instance.
        
        Args:
            name (str): The name of the card
            description (str): The description of the card
            image_path (str): Path to the card's image file
            effect (Callable): Function to be executed when card is activated
            **new_params: Additional attributes for specific game mechanics
                Common examples:
                - level: Card's level/rank
                - cost: Resource cost to play
                - type: Card type/category
                - rarity: Card rarity
        """
        self.__effect = effect
        self.__owner = None
        self.__visuals = None
        self.__attributes = new_params
        self.__name = name
        self.__description = description
        self.__image_path = image_path
    
    def init_visuals(self, width: int, height: int, 
                    color: tuple[int, int, int] = (255, 255, 255),
                    scale: float = 1.0) -> None:
        """
        Initialize visual representation for the card.
        
        Args:
            width (int): Card width in pixels
            height (int): Card height in pixels
            color (tuple[int, int, int], optional): Card background color. Defaults to white
            scale (float, optional): Initial scale factor. Defaults to 1.0
        """
        surface = Surface((width, height), SRCALPHA)
        surface.fill(color)
        self.__visuals = CardVisuals(
            surface=surface,
            rect=Rect(0, 0, width, height),
            scale=scale
        )
    
    def __blit__(self, window, pos: tuple[int, int], **kwargs) -> None:
        """
        Draw the card on the window.
        
        Args:
            window: The window to draw on
            pos (tuple[int, int]): Position to draw the card
            **kwargs: Additional drawing parameters
        """
        if not self.__visuals:
            return
            
        # Apply transformations
        surface = self.__visuals.surface
        if self.__visuals.scale != 1.0:
            new_size = (int(surface.get_width() * self.__visuals.scale),
                       int(surface.get_height() * self.__visuals.scale))
            surface = pg.transform.scale(surface, new_size)
            
        if self.__visuals.rotation != 0:
            surface = pg.transform.rotate(surface, self.__visuals.rotation)
            
        if self.__visuals.alpha != 255:
            surface.set_alpha(self.__visuals.alpha)
            
        # Update rect position
        self.__visuals.rect.center = pos
        
        # Draw to window
        window.blit(surface, pos)
    
    def __activate__(self, owner, *args, **kwargs) -> Any:
        """
        Activate the card's effect.
        
        Args:
            *args: Arguments to pass to the effect function
            **kwargs: Keyword arguments to pass to the effect function
            
        Returns:
            Any: Result of the effect function
            
        Raises:
            ValueError: If card has no owner
        """
        if not self.__owner:
            raise ValueError("Card must have an owner to be activated")
        if not self.__owner == owner: 
            raise ValueError(f"Card must be used by its owner, not {owner}")
        return self.__effect(*args, **kwargs)
    
    def collect(self, new_owner: Any) -> None:
        """
        Change the card's owner.
        
        Args:
            new_owner (Any): The new owner of the card
        """
        self.__owner = new_owner
    
    def discard(self) -> None:
        """Remove the card's owner."""
        self.__owner = None
    
    @property
    def owner(self) -> Any:
        """Get the current owner of the card."""
        return self.__owner
    
    @property
    def visuals(self) -> Optional[CardVisuals]:
        """Get the card's visual properties if initialized."""
        return self.__visuals
    
    def get_attribute(self, name: str, default: Any = None) -> Any:
        """
        Get a custom attribute value.
        
        Args:
            name (str): Attribute name
            default (Any, optional): Default value if attribute doesn't exist
            
        Returns:
            Any: Attribute value or default
        """
        return self.__attributes.get(name, default)
    
    def set_attribute(self, name: str, value: Any) -> None:
        """
        Set a custom attribute value.
        
        Args:
            name (str): Attribute name
            value (Any): New attribute value
        """
        self.__attributes[name] = value

    @property
    def name(self) -> str:
        """Get the name of the card."""
        return self.__name

    @property
    def description(self) -> str:
        """Get the description of the card."""
        return self.__description

    @property
    def image_path(self) -> str:
        """Get the path to the card's image."""
        return self.__image_path

    
