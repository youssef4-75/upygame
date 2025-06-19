"""
ParticleSystem module for creating and managing particle effects.

This module provides the ParticleSystem class which handles particle emission,
physics, and rendering for various visual effects like explosions, smoke, etc.
"""

from typing import List, Tuple
from pygame import Surface, Vector2, Color, transform
from dataclasses import dataclass
import random
import math

@dataclass
class ParticleProperties:
    """Data class for particle properties"""
    lifetime: float  # Total lifetime in seconds
    start_color: Color  # Starting color
    end_color: Color  # Ending color
    start_size: float  # Starting size
    end_size: float  # Ending size
    start_speed: float  # Starting speed
    end_speed: float  # Ending speed
    gravity_scale: float = 0.0  # Gravity effect on particle
    drag: float = 0.0  # Air resistance
    rotation_speed: float = 0.0  # Rotation speed in degrees per second
    fade_out: bool = True  # Whether to fade out at end of life

class Particle:
    """
    A single particle in the system.
    
    Attributes:
        position (Vector2): Current position
        velocity (Vector2): Current velocity
        color (Color): Current color
        size (float): Current size
        rotation (float): Current rotation in degrees
        age (float): Current age in seconds
        properties (ParticleProperties): Particle properties
    """
    
    def __init__(self, position: Vector2, direction: Vector2, 
                properties: ParticleProperties) -> None:
        """
        Initialize a particle.
        
        Args:
            position (Vector2): Starting position
            direction (Vector2): Initial direction
            properties (ParticleProperties): Particle properties
        """
        self.position = Vector2(position)
        self.velocity = direction.normalize() * properties.start_speed
        self.color = Color(properties.start_color)
        self.size = properties.start_size
        self.rotation = 0.0
        self.age = 0.0
        self.properties = properties
    
    def update(self, dt: float) -> bool:
        """
        Update particle state.
        
        Args:
            dt (float): Time delta since last update
            
        Returns:
            bool: True if particle is still alive, False if it should be removed
        """
        self.age += dt
        if self.age >= self.properties.lifetime:
            return False
            
        # Update position and velocity
        self.velocity.y += self.properties.gravity_scale * dt
        self.velocity *= (1 - self.properties.drag * dt)
        self.position += self.velocity * dt
        
        # Update rotation
        self.rotation += self.properties.rotation_speed * dt
        
        # Update size
        progress = self.age / self.properties.lifetime
        self.size = self.properties.start_size + (self.properties.end_size - self.properties.start_size) * progress
        
        # Update color
        if self.properties.fade_out:
            alpha = int(255 * (1 - progress))
            self.color.a = alpha
        else:
            self.color = self.properties.start_color.lerp(self.properties.end_color, progress)
            
        return True
    
    def draw(self, surface: Surface) -> None:
        """
        Draw the particle to the surface.
        
        Args:
            surface (Surface): Surface to draw on
        """
        # Create a small surface for the particle
        size = int(self.size * 2)
        if size < 1:
            return
            
        particle_surface = Surface((size, size))
        particle_surface.fill(self.color)
        
        # Rotate if needed
        if self.rotation != 0:
            particle_surface = transform.rotate(particle_surface, self.rotation)
            
        # Draw to main surface
        surface.blit(particle_surface, 
                    (self.position.x - size/2, self.position.y - size/2))

class ParticleSystem:
    """
    A system for managing and rendering particles.
    
    This class handles particle emission, physics simulation, and rendering
    for various visual effects. It supports different emission patterns and
    particle behaviors.
    
    Attributes:
        __particles (List[Particle]): List of active particles
        __emission_rate (float): Particles per second
        __emission_radius (float): Radius for random emission
        __gravity (Vector2): Global gravity vector
    """
    
    def __init__(self, emission_rate: float = 10.0, 
                 emission_radius: float = 0.0,
                 gravity: Tuple[float, float] = (0, 9.81)) -> None:
        """
        Initialize the particle system.
        
        Args:
            emission_rate (float, optional): Particles per second. Defaults to 10.0
            emission_radius (float, optional): Radius for random emission. Defaults to 0.0
            gravity (Tuple[float, float], optional): Global gravity. Defaults to (0, 9.81)
        """
        self.__particles: List[Particle] = []
        self.__emission_rate = emission_rate
        self.__emission_radius = emission_radius
        self.__gravity = Vector2(gravity)
        self.__emission_accumulator = 0.0
    
    def emit(self, position: Vector2, direction: Vector2,
             properties: ParticleProperties, count: int = 1) -> None:
        """
        Emit particles from a position.
        
        Args:
            position (Vector2): Emission position
            direction (Vector2): Base emission direction
            properties (ParticleProperties): Particle properties
            count (int, optional): Number of particles to emit. Defaults to 1
        """
        for _ in range(count):
            # Add random offset to position if emission radius > 0
            if self.__emission_radius > 0:
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(0, self.__emission_radius)
                offset = Vector2(math.cos(angle), math.sin(angle)) * radius
                pos = position + offset
            else:
                pos = position
                
            # Add random variation to direction
            angle = random.uniform(-math.pi/4, math.pi/4)
            dir = direction.rotate(angle)
            
            self.__particles.append(Particle(pos, dir, properties))
    
    def update(self, dt: float) -> None:
        """
        Update all particles.
        
        Args:
            dt (float): Time delta since last update
        """
        # Update existing particles
        self.__particles = [p for p in self.__particles if p.update(dt)]
    
    def draw(self, surface: Surface) -> None:
        """
        Draw all particles to the surface.
        
        Args:
            surface (Surface): Surface to draw on
        """
        for particle in self.__particles:
            particle.draw(surface)
    
    def clear(self) -> None:
        """Remove all particles from the system."""
        self.__particles.clear()
    
    @property
    def particle_count(self) -> int:
        """Get the current number of particles."""
        return len(self.__particles)
    
    def set_emission_rate(self, rate: float) -> None:
        """
        Set the emission rate.
        
        Args:
            rate (float): New emission rate in particles per second
        """
        self.__emission_rate = rate
    
    def set_emission_radius(self, radius: float) -> None:
        """
        Set the emission radius.
        
        Args:
            radius (float): New emission radius
        """
        self.__emission_radius = radius 