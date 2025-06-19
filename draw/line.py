"""
Glow line module for creating realistic glowing line effects.

This module provides the glow_line function which creates a glowing line effect
with customizable properties like width, color, vibration, and glow intensity.
"""

from pygame import draw, Surface, Vector2
from numpy import linspace, arange
from random import normalvariate as nv, randint
from typing import Any, Optional
from icecream import ic

from .color import uColor
from ..window.window import Window

def glow_line(
        surface: Surface|Window,
        key: Any,
        color: uColor,
        start_pos: tuple[int, int],
        end_pos: tuple[int, int],
        *,
        max_width: int = 3,
        min_width: int = 0,
        vibration: int = 0,
        essence_color: Optional[uColor] = None,
        main_layers: int = 3,
        aura: float = 0.0,  # aura is now optional and off by default
        aura_layers: int = 5,
        aura_intensity: float = .7,
        aura_vibration: int = 10,
        **_
) -> None:
    """
    Draw a glowing line with multilayer core and optional aura.
    Args:
        surface: Surface or Window to draw on
        key: Layer key if using Window
        color: Base color of the line
        start_pos: Starting position (x, y)
        end_pos: Ending position (x, y)
        min_width: Minimum width of the core line
        max_width: Maximum width of the core line
        essence_color: Color to blend with for gradient effect (outermost core layer)
        main_layers: Number of core layers
        aura: Size of the aura (0 disables aura)
        aura_layers: Number of aura layers
        aura_intensity: Intensity of the aura (0-1)
        core_opacity: Opacity of the core line (0-1)
    """
    if essence_color is None:
        essence_color = color
    
    if not isinstance(surface, Surface):
        if key in surface.layers:
            surface = surface.layers[key]
        else:
            surface = surface.screen
        assert isinstance(surface, Surface)

    vib_ratio = randint(0, int(vibration))
    vib_aura_ratio = randint(0, int(aura_vibration))
    min_width += vib_ratio
    max_width += vib_ratio
    if aura: aura += vib_aura_ratio


    # Optional aura (drawn outside the main line, with fading alpha)
    if aura > 0 and aura_layers > 0:
        for i in range(aura_layers):
            t = i / max(aura_layers - 1, 1)
            width = int(max_width + aura * (2 - t))
            # Aura color is a faded version of essence_color
            aura_alpha = aura_intensity * (1-t/2)
            print(aura_alpha)
            aura_color = uColor.opacity(essence_color, aura_alpha)
            draw.line(surface, aura_color, start_pos, end_pos, width=width)

    
    # Draw multilayer main line (from thickest to thinnest)
    for i in range(main_layers):
        t = i / max(main_layers - 1, 1)
        tp = min(i, main_layers - 1) / max(main_layers - 2, 1)
        width = int(max_width * (1 - t) + min_width * t)
        # Interpolate color from essence_color (outer) to color (inner)
        layer_color = (1 - tp) * color + tp * essence_color
        # layer_color = uColor.opacity(layer_color, core_opacity)
        draw.line(surface, layer_color, start_pos, end_pos, width=width)

    