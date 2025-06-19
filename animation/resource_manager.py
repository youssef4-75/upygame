"""
ResourceManager module for efficient game resource management.

This module provides the ResourceManager class which handles loading, caching,
and managing game resources like images, sounds, and fonts.
"""

from typing import Dict, Any, Optional, TypeVar, Generic, Callable
from pygame import Surface, image, mixer, font
from pygame.surface import Surface
from pygame.mixer import Sound
from pygame.font import Font
import os
from pathlib import Path
import json
from dataclasses import dataclass
from threading import Lock

T = TypeVar('T')

@dataclass
class ResourceMetadata:
    """Metadata for a loaded resource"""
    path: str
    last_modified: float
    size: int
    type: str

class ResourceCache(Generic[T]):
    """
    A generic cache for game resources.
    
    This class handles caching of resources with automatic cleanup
    and memory management.
    
    Attributes:
        __cache (Dict[str, T]): The resource cache
        __metadata (Dict[str, ResourceMetadata]): Resource metadata
        __max_size (int): Maximum cache size in bytes
        __current_size (int): Current cache size in bytes
        __lock (Lock): Thread lock for thread safety
    """
    
    def __init__(self, max_size: int = 100 * 1024 * 1024) -> None:  # 100MB default
        """
        Initialize the resource cache.
        
        Args:
            max_size (int, optional): Maximum cache size in bytes. Defaults to 100MB
        """
        self.__cache: Dict[str, T] = {}
        self.__metadata: Dict[str, ResourceMetadata] = {}
        self.__max_size = max_size
        self.__current_size = 0
        self.__lock = Lock()
    
    def get(self, key: str) -> Optional[T]:
        """
        Get a resource from the cache.
        
        Args:
            key (str): Resource key
            
        Returns:
            Optional[T]: The cached resource or None if not found
        """
        with self.__lock:
            return self.__cache.get(key)
    
    def put(self, key: str, resource: T, metadata: ResourceMetadata) -> None:
        """
        Add a resource to the cache.
        
        Args:
            key (str): Resource key
            resource (T): Resource to cache
            metadata (ResourceMetadata): Resource metadata
        """
        with self.__lock:
            # Remove old resource if it exists
            if key in self.__cache:
                self.__current_size -= self.__metadata[key].size
                del self.__cache[key]
                del self.__metadata[key]
            
            # Check if we need to make space
            while self.__current_size + metadata.size > self.__max_size:
                if not self.__cache:
                    return  # Cache is empty but still not enough space
                # Remove least recently used resource
                oldest_key = min(self.__metadata.items(), 
                               key=lambda x: x[1].last_modified)[0]
                self.__current_size -= self.__metadata[oldest_key].size
                del self.__cache[oldest_key]
                del self.__metadata[oldest_key]
            
            # Add new resource
            self.__cache[key] = resource
            self.__metadata[key] = metadata
            self.__current_size += metadata.size
    
    def remove(self, key: str) -> None:
        """
        Remove a resource from the cache.
        
        Args:
            key (str): Resource key to remove
        """
        with self.__lock:
            if key in self.__cache:
                self.__current_size -= self.__metadata[key].size
                del self.__cache[key]
                del self.__metadata[key]
    
    def clear(self) -> None:
        """Clear all resources from the cache."""
        with self.__lock:
            self.__cache.clear()
            self.__metadata.clear()
            self.__current_size = 0
    
    @property
    def size(self) -> int:
        """Get the current cache size in bytes."""
        return self.__current_size
    
    @property
    def max_size(self) -> int:
        """Get the maximum cache size in bytes."""
        return self.__max_size
    
    def set_max_size(self, size: int) -> None:
        """
        Set the maximum cache size.
        
        Args:
            size (int): New maximum size in bytes
        """
        with self.__lock:
            self.__max_size = size
            # Trim cache if necessary
            while self.__current_size > self.__max_size:
                if not self.__cache:
                    break
                oldest_key = min(self.__metadata.items(), 
                               key=lambda x: x[1].last_modified)[0]
                self.__current_size -= self.__metadata[oldest_key].size
                del self.__cache[oldest_key]
                del self.__metadata[oldest_key]

class ResourceManager:
    """
    A manager for game resources with efficient caching.
    
    This class handles loading, caching, and managing various types of
    game resources including images, sounds, and fonts. It provides
    automatic resource cleanup and memory management.
    
    Attributes:
        __image_cache (ResourceCache[Surface]): Cache for image resources
        __sound_cache (ResourceCache[Sound]): Cache for sound resources
        __font_cache (ResourceCache[Font]): Cache for font resources
        __resource_paths (Dict[str, str]): Mapping of resource keys to file paths
    """
    
    def __init__(self, base_path: str = "assets") -> None:
        """
        Initialize the resource manager.
        
        Args:
            base_path (str, optional): Base path for resources. Defaults to "assets"
        """
        self.__base_path = Path(base_path)
        self.__image_cache = ResourceCache[Surface]()
        self.__sound_cache = ResourceCache[Sound]()
        self.__font_cache = ResourceCache[Font]()
        self.__resource_paths: Dict[str, str] = {}
        
        # Create base directories if they don't exist
        self.__base_path.mkdir(parents=True, exist_ok=True)
        (self.__base_path / "images").mkdir(exist_ok=True)
        (self.__base_path / "sounds").mkdir(exist_ok=True)
        (self.__base_path / "fonts").mkdir(exist_ok=True)
    
    def load_image(self, key: str, path: str, 
                  convert_alpha: bool = True) -> Optional[Surface]:
        """
        Load an image resource.
        
        Args:
            key (str): Resource key
            path (str): Path to image file
            convert_alpha (bool, optional): Whether to convert with alpha. Defaults to True
            
        Returns:
            Optional[Surface]: Loaded image surface or None if loading failed
        """
        try:
            full_path = self.__base_path / "images" / path
            if not full_path.exists():
                return None
                
            # Check if already cached
            cached = self.__image_cache.get(key)
            if cached:
                return cached
            
            # Load and cache new image
            img = image.load(str(full_path))
            if convert_alpha:
                img = img.convert_alpha()
            else:
                img = img.convert()
            
            metadata = ResourceMetadata(
                path=str(full_path),
                last_modified=full_path.stat().st_mtime,
                size=img.get_width() * img.get_height() * 4,  # Approximate size
                type="image"
            )
            
            self.__image_cache.put(key, img, metadata)
            self.__resource_paths[key] = str(full_path)
            return img
            
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def load_sound(self, key: str, path: str) -> Optional[Sound]:
        """
        Load a sound resource.
        
        Args:
            key (str): Resource key
            path (str): Path to sound file
            
        Returns:
            Optional[Sound]: Loaded sound or None if loading failed
        """
        try:
            full_path = self.__base_path / "sounds" / path
            if not full_path.exists():
                return None
                
            # Check if already cached
            cached = self.__sound_cache.get(key)
            if cached:
                return cached
            
            # Load and cache new sound
            sound = mixer.Sound(str(full_path))
            
            metadata = ResourceMetadata(
                path=str(full_path),
                last_modified=full_path.stat().st_mtime,
                size=full_path.stat().st_size,
                type="sound"
            )
            
            self.__sound_cache.put(key, sound, metadata)
            self.__resource_paths[key] = str(full_path)
            return sound
            
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
            return None
    
    def load_font(self, key: str, path: str, size: int) -> Optional[Font]:
        """
        Load a font resource.
        
        Args:
            key (str): Resource key
            path (str): Path to font file
            size (int): Font size
            
        Returns:
            Optional[Font]: Loaded font or None if loading failed
        """
        try:
            full_path = self.__base_path / "fonts" / path
            if not full_path.exists():
                return None
                
            # Check if already cached
            cached = self.__font_cache.get(key)
            if cached:
                return cached
            
            # Load and cache new font
            font_obj = font.Font(str(full_path), size)
            
            metadata = ResourceMetadata(
                path=str(full_path),
                last_modified=full_path.stat().st_mtime,
                size=full_path.stat().st_size,
                type="font"
            )
            
            self.__font_cache.put(key, font_obj, metadata)
            self.__resource_paths[key] = str(full_path)
            return font_obj
            
        except Exception as e:
            print(f"Error loading font {path}: {e}")
            return None
    
    def get_resource_path(self, key: str) -> Optional[str]:
        """
        Get the file path for a resource.
        
        Args:
            key (str): Resource key
            
        Returns:
            Optional[str]: Resource file path or None if not found
        """
        return self.__resource_paths.get(key)
    
    def clear_cache(self, resource_type: Optional[str] = None) -> None:
        """
        Clear resource cache.
        
        Args:
            resource_type (Optional[str], optional): Type of resources to clear.
                If None, clears all caches. Defaults to None
        """
        if resource_type is None or resource_type == "image":
            self.__image_cache.clear()
        if resource_type is None or resource_type == "sound":
            self.__sound_cache.clear()
        if resource_type is None or resource_type == "font":
            self.__font_cache.clear()
    
    def set_cache_size(self, size: int, resource_type: Optional[str] = None) -> None:
        """
        Set maximum cache size.
        
        Args:
            size (int): Maximum size in bytes
            resource_type (Optional[str], optional): Type of resources to set size for.
                If None, sets size for all caches. Defaults to None
        """
        if resource_type is None or resource_type == "image":
            self.__image_cache.set_max_size(size)
        if resource_type is None or resource_type == "sound":
            self.__sound_cache.set_max_size(size)
        if resource_type is None or resource_type == "font":
            self.__font_cache.set_max_size(size)
    
    def get_cache_size(self, resource_type: Optional[str] = None) -> int:
        """
        Get current cache size.
        
        Args:
            resource_type (Optional[str], optional): Type of resources to get size for.
                If None, returns total size. Defaults to None
                
        Returns:
            int: Current cache size in bytes
        """
        size = 0
        if resource_type is None or resource_type == "image":
            size += self.__image_cache.size
        if resource_type is None or resource_type == "sound":
            size += self.__sound_cache.size
        if resource_type is None or resource_type == "font":
            size += self.__font_cache.size
        return size 