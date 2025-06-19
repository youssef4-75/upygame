"""
SpriteManager module for handling game sprites, collisions, and physics.

This module provides the SpriteManager class which manages game sprites with
features like collision detection, physics simulation, and sprite grouping.
"""

from typing import Dict, List, Set, Tuple, Optional
from pygame import Surface, Rect, sprite, Vector2
from pygame.sprite import Group, Sprite
from dataclasses import dataclass
from enum import Enum, auto

class Layer(Enum):
    """Enum for sprite rendering layers"""
    BACKGROUND = auto()
    TERRAIN = auto()
    DECORATION = auto()
    ENTITY = auto()
    FOREGROUND = auto()
    UI = auto()

@dataclass
class PhysicsProperties:
    """Data class for sprite physics properties"""
    mass: float = 1.0
    friction: float = 0.1
    restitution: float = 0.5  # bounciness
    gravity_scale: float = 1.0
    is_static: bool = False

class SpriteManager:
    """
    A class to manage game sprites with collision detection and physics.
    
    This class handles sprite grouping, collision detection, basic physics
    simulation, and sprite state management. It supports multiple rendering
    layers and efficient collision checking.
    
    Attributes:
        __layers (Dict[Layer, Group]): Dictionary of sprite groups by layer
        __physics_props (Dict[Sprite, PhysicsProperties]): Physics properties for sprites
        __collision_groups (Dict[str, Set[Sprite]]): Groups for collision checking
        __gravity (Vector2): Global gravity vector
        __active_sprites (Set[Sprite]): Set of currently active sprites
    """
    
    def __init__(self, gravity: Tuple[float, float] = (0, 9.81)) -> None:
        """
        Initialize the SpriteManager.
        
        Args:
            gravity (Tuple[float, float], optional): Global gravity vector. Defaults to (0, 9.81)
        """
        self.__layers: Dict[Layer, Group] = {layer: Group() for layer in Layer}
        self.__physics_props: Dict[Sprite, PhysicsProperties] = {}
        self.__collision_groups: Dict[str, Set[Sprite]] = {}
        self.__gravity = Vector2(gravity)
        self.__active_sprites: Set[Sprite] = set()
    
    def add_sprite(self, sprite: Sprite, layer: Layer = Layer.ENTITY, 
                  physics_props: Optional[PhysicsProperties] = None,
                  collision_groups: List[str] = None) -> None:
        """
        Add a sprite to the manager.
        
        Args:
            sprite (Sprite): The sprite to add
            layer (Layer, optional): Rendering layer. Defaults to Layer.ENTITY
            physics_props (PhysicsProperties, optional): Physics properties. Defaults to None
            collision_groups (List[str], optional): Collision groups. Defaults to None
        """
        self.__layers[layer].add(sprite)
        self.__active_sprites.add(sprite)
        
        if physics_props:
            self.__physics_props[sprite] = physics_props
            
        if collision_groups:
            for group in collision_groups:
                if group not in self.__collision_groups:
                    self.__collision_groups[group] = set()
                self.__collision_groups[group].add(sprite)
    
    def remove_sprite(self, sprite: Sprite) -> None:
        """
        Remove a sprite from the manager.
        
        Args:
            sprite (Sprite): The sprite to remove
        """
        for layer in self.__layers.values():
            if sprite in layer:
                layer.remove(sprite)
        
        self.__active_sprites.discard(sprite)
        self.__physics_props.pop(sprite, None)
        
        for group in self.__collision_groups.values():
            group.discard(sprite)
    
    def update(self, dt: float) -> None:
        """
        Update all sprites and handle physics.
        
        Args:
            dt (float): Time delta since last update
        """
        # Update physics
        for sprite in self.__active_sprites:
            if sprite in self.__physics_props:
                props = self.__physics_props[sprite]
                if not props.is_static:
                    # Apply gravity
                    sprite.velocity += self.__gravity * props.gravity_scale * dt
                    
                    # Update position
                    sprite.rect.x += sprite.velocity.x * dt
                    sprite.rect.y += sprite.velocity.y * dt
                    
                    # Apply friction
                    sprite.velocity *= (1 - props.friction)
        
        # Check collisions
        self.__check_collisions()
        
        # Update all layers
        for layer in self.__layers.values():
            layer.update()
    
    def __check_collisions(self) -> None:
        """Check for collisions between sprites in collision groups."""
        for group_name, sprites in self.__collision_groups.items():
            for sprite1 in sprites:
                for sprite2 in sprites:
                    if sprite1 != sprite2 and sprite1.rect.colliderect(sprite2.rect):
                        self.__resolve_collision(sprite1, sprite2)
    
    def __resolve_collision(self, sprite1: Sprite, sprite2: Sprite) -> None:
        """
        Resolve collision between two sprites.
        
        Args:
            sprite1 (Sprite): First sprite in collision
            sprite2 (Sprite): Second sprite in collision
        """
        if sprite1 not in self.__physics_props or sprite2 not in self.__physics_props:
            return
            
        props1 = self.__physics_props[sprite1]
        props2 = self.__physics_props[sprite2]
        
        if props1.is_static and props2.is_static:
            return
            
        # Calculate collision normal and penetration depth
        rect1, rect2 = sprite1.rect, sprite2.rect
        overlap_x = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
        overlap_y = min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top)
        
        if overlap_x < overlap_y:
            normal = Vector2(1 if rect1.centerx < rect2.centerx else -1, 0)
            penetration = overlap_x
        else:
            normal = Vector2(0, 1 if rect1.centery < rect2.centery else -1)
            penetration = overlap_y
            
        # Resolve collision
        if not props1.is_static:
            sprite1.rect.x += normal.x * penetration * 0.5
            sprite1.rect.y += normal.y * penetration * 0.5
            
            # Calculate new velocities
            relative_velocity = sprite1.velocity - sprite2.velocity
            velocity_along_normal = relative_velocity.dot(normal)
            
            if velocity_along_normal < 0:
                restitution = min(props1.restitution, props2.restitution)
                impulse = -(1 + restitution) * velocity_along_normal
                impulse /= props1.mass + props2.mass
                
                sprite1.velocity += normal * impulse * props1.mass
                
        if not props2.is_static:
            sprite2.rect.x -= normal.x * penetration * 0.5
            sprite2.rect.y -= normal.y * penetration * 0.5
            
            if not props1.is_static:
                sprite2.velocity -= normal * impulse * props2.mass
    
    def draw(self, surface: Surface) -> None:
        """
        Draw all sprites to the given surface.
        
        Args:
            surface (Surface): The surface to draw on
        """
        for layer in Layer:
            self.__layers[layer].draw(surface)
    
    def get_sprites_in_rect(self, rect: Rect, layer: Optional[Layer] = None) -> List[Sprite]:
        """
        Get all sprites that intersect with the given rectangle.
        
        Args:
            rect (Rect): The rectangle to check
            layer (Layer, optional): Layer to check. Defaults to None (all layers)
            
        Returns:
            List[Sprite]: List of sprites that intersect with the rectangle
        """
        sprites = []
        if layer:
            for sprite in self.__layers[layer]:
                if sprite.rect.colliderect(rect):
                    sprites.append(sprite)
        else:
            for layer_group in self.__layers.values():
                for sprite in layer_group:
                    if sprite.rect.colliderect(rect):
                        sprites.append(sprite)
        return sprites 