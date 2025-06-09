from pygame import draw, Surface, Vector2
from numpy import linspace, arange
from icecream import ic
from random import normalvariate as nv
from typing import Any

from ..color import uColor

from ...window import Window


def glow_line(
        surface: Surface|Window,
        key: Any,
        color: uColor,
        start_pos: tuple[int, int],
        end_pos: tuple[int, int],
        *,
        width: int = 1,
        essence_color: uColor|None = None,
        vibration = 4, 
        aura = 1,
        gradientX = 20,
        step = 20,
):
    
    
    # TODO: assert the opacity of these lines
    # PROBLEM: draw.line function doesn't consider opacity dimension in colors
        
    if essence_color is None: essence_color = color
    if not isinstance(surface, Surface): 
        if key in surface.layers:
            surface = surface.layers[key]
        else: 
            surface = surface.screen
        assert isinstance(surface, Surface)

    rstart = Vector2(start_pos[0], start_pos[1])
    rend = Vector2(rstart[0], rstart[1])
    _dir = Vector2(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    r = _dir.magnitude()
    try: _dir.normalize_ip()
    except ValueError: ...
    
    for _per in arange(0, r-2*step, 2*step):
        
        vib = max(nv(0, vibration), 0)

        rstart = rend
        rend = rend + step*_dir
        
        per = float(_per)

        rstart = rend
        rend = rend + step*_dir
        
        _color = uColor.opacity(color, min(abs(vib), 1)/2)
        iwidth = int(aura + width + vib)
        draw.line(surface, _color, rstart, rend, width=iwidth)


    for _per in linspace(1, 0, gradientX):
        per = float(_per)
        med_color = per * color + (1 - per) * essence_color
    
        iwidth = int(per*width)
        draw.line(surface, med_color, start_pos, end_pos, width=iwidth)
    

    