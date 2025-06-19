from pygame import draw
import pygame


def glow(func):
    def draw_glowing(*args, glow_radius=5, glow_color=None, glow_alpha=80, **kwargs):
        # Extract surface and color from args
    
        color = args[1] if len(args) > 1 else kwargs.get('color', (255,255,255))
        # Use glow_color or fallback to color
        base_glow_color = glow_color if glow_color is not None else color
        # Draw glow layers (from outer to inner)
        for i in range(glow_radius, 0, -1):
            alpha = int(glow_alpha * (i / glow_radius))
            # Create a color with alpha (if using pygame.Color)
            if isinstance(base_glow_color, pygame.Color):
                glow_col = base_glow_color
                glow_col.a = alpha
            else:
                # Assume RGB tuple
                if len(base_glow_color) == 4:
                    glow_col = (*base_glow_color[:3], alpha)
                else:
                    glow_col = (*base_glow_color, alpha)
            # For line/rect/circle, width is usually the last arg
            new_args = list(args)
            if func.__name__ in ('line', 'rect', 'ellipse', 'arc'):
                if 'width' in kwargs:
                    kwargs['width'] = kwargs.get('width', 1) + i * 2
                elif len(new_args) > 4:
                    new_args[-1] = new_args[-1] + i * 2
                else:
                    kwargs['width'] = 1 + i * 2
            # Set color
            if len(new_args) > 1:
                new_args[1] = glow_col
            else:
                kwargs['color'] = glow_col
            func(*new_args, **kwargs)
        # Draw the core shape
        return func(*args, **kwargs)
    return draw_glowing
