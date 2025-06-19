"""
This directory contains classes for game development with Pygame.

The module provides several key classes:
- Animation: For managing frame-based animations
- AnimationSet: For managing collections of animations with priority-based transitions
- SpriteManager: For managing game sprites with collision detection and physics
- ParticleSystem: For creating and managing particle effects
- ResourceManager: For efficient loading and caching of game resources
"""

from .animation import Animation
from .animation_set import AnimationSet
from .sprite_manager import SpriteManager, Layer, PhysicsProperties
from .particle_system import ParticleSystem, ParticleProperties
from .resource_manager import ResourceManager, ResourceCache, ResourceMetadata

__all__ = [
    'Animation',
    'AnimationSet',
    'SpriteManager',
    'Layer',
    'PhysicsProperties',
    'ParticleSystem',
    'ParticleProperties',
    'ResourceManager',
    'ResourceCache',
    'ResourceMetadata'
]
