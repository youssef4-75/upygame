"""
Deck module for managing collections of cards in various types of games.

This module provides the Deck class which represents a collection of cards with
support for drawing, shuffling, and card management operations.
"""

from typing import List, Optional, Callable, Any
import random
from .card import Card


class Deck[T]:
    """
    A class to represent a deck of cards with comprehensive management functionality.
    
    This class provides methods for drawing cards, shuffling, and managing the deck's
    contents. It supports generic typing to ensure type safety with different card types.
    
    Attributes:
        __cards (List[T]): List of cards in the deck
        __max_size (int): Maximum number of cards allowed
        __draw_callback (Optional[Callable[[T], None]]): Function to call when drawing cards
        __shuffle_callback (Optional[Callable[[List[T]], None]]): Function to call when shuffling
        __owner (Any): Owner of the deck
    """
    
    def __init__(self, max_size: int = 60,
                 draw_callback: Callable[[T], None]|None = None,
                 shuffle_callback: Callable[[List[T]], None]|None = None) -> None:
        """
        Initialize a Deck instance.
        
        Args:
            max_size (int, optional): Maximum number of cards allowed. Defaults to 60.
            draw_callback (Optional[Callable[[T], None]], optional): Function to call when drawing cards
            shuffle_callback (Optional[Callable[[List[T]], None]], optional): Function to call when shuffling
        """
        self.__cards: List[T] = []
        self.__max_size = max_size
        self.__draw_callback = draw_callback
        self.__shuffle_callback = shuffle_callback
        self.__owner = None
    
    def add_card(self, card: T) -> bool:
        """
        Add a card to the deck.
        
        Args:
            card (T): The card to add
            
        Returns:
            bool: True if the card was added successfully, False if deck is full
        """
        if len(self.__cards) >= self.__max_size:
            return False
        self.__cards.append(card)
        return True
    
    def remove_card(self, card: T) -> bool:
        """
        Remove a card from the deck.
        
        Args:
            card (T): The card to remove
            
        Returns:
            bool: True if the card was removed successfully, False if card not found
        """
        try:
            self.__cards.remove(card)
            return True
        except ValueError:
            return False
    
    def draw_card(self) -> Optional[T]:
        """
        Draw a card from the top of the deck.
        
        Returns:
            Optional[T]: The drawn card, or None if deck is empty
        """
        if not self.__cards:
            return None
        card = self.__cards.pop()
        if self.__draw_callback:
            self.__draw_callback(card)
        return card
    
    def draw_random(self) -> Optional[T]:
        """
        Draw a random card from the deck.
        
        Returns:
            Optional[T]: The drawn card, or None if deck is empty
        """
        if not self.__cards:
            return None
        card = random.choice(self.__cards)
        self.__cards.remove(card)
        if self.__draw_callback:
            self.__draw_callback(card)
        return card
    
    def draw_specific(self, card: T) -> bool:
        """
        Draw a specific card from the deck.
        
        Args:
            card (T): The card to draw
            
        Returns:
            bool: True if the card was drawn successfully, False if card not found
        """
        if card in self.__cards:
            self.__cards.remove(card)
            if self.__draw_callback:
                self.__draw_callback(card)
            return True
        return False
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.__cards)
        if self.__shuffle_callback:
            self.__shuffle_callback(self.__cards)
    
    def clear(self) -> None:
        """Remove all cards from the deck."""
        self.__cards.clear()
    
    def get_card(self, index: int) -> Optional[T]:
        """
        Get a card at a specific index.
        
        Args:
            index (int): The index of the card to get
            
        Returns:
            Optional[T]: The card at the specified index, or None if index is invalid
        """
        try:
            return self.__cards[index]
        except IndexError:
            return None
    
    def find_card(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Find a card matching a predicate.
        
        Args:
            predicate (Callable[[T], bool]): Function that returns True for matching cards
            
        Returns:
            Optional[T]: The first matching card, or None if no match found
        """
        for card in self.__cards:
            if predicate(card):
                return card
        return None
    
    def filter_cards(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Get all cards matching a predicate.
        
        Args:
            predicate (Callable[[T], bool]): Function that returns True for matching cards
            
        Returns:
            List[T]: List of all matching cards
        """
        return [card for card in self.__cards if predicate(card)]
    
    def set_owner(self, owner: Any) -> None:
        """
        Set the deck's owner.
        
        Args:
            owner (Any): The new owner of the deck
        """
        self.__owner = owner
    
    @property
    def owner(self) -> Any:
        """Get the current owner of the deck."""
        return self.__owner
    
    @property
    def size(self) -> int:
        """Get the current number of cards in the deck."""
        return len(self.__cards)
    
    @property
    def is_empty(self) -> bool:
        """Check if the deck is empty."""
        return len(self.__cards) == 0
    
    @property
    def is_full(self) -> bool:
        """Check if the deck is at maximum capacity."""
        return len(self.__cards) >= self.__max_size
    
    def __iter__(self):
        """Support iteration over cards in the deck."""
        return iter(self.__cards)
    
    def __contains__(self, card: T) -> bool:
        """
        Check if a card is in the deck.
        
        Args:
            card (T): The card to check for
            
        Returns:
            bool: True if the card is in the deck, False otherwise
        """
        return card in self.__cards