from typing import Callable, Any
import pygame as pg
from multipledispatch import dispatch
import math

from ..animation import AnimationSet
from ..board import Board


class Window:
    """
    A window class that manages the pygame display and provides additional functionality
    like layers, event handling, and drawing utilities.
    
    Layers and camera are optional and must be initialized using init_layers() and init_camera()
    before using their respective functions.
    """
    def __init__(self, 
                title: str,
                width: int, 
                height: int, 
                *loop_phases: Callable, 
                with_layers=False, 
                with_camera=False,
                default_color=3*(255,)):
        """
        Initialize a new Window instance.
        
        Args:
            title (str): The window title
            width (int): Window width in pixels
            height (int): Window height in pixels
            *loop_phases: Optional callback functions to be executed in the game loop
            with_layers (bool): Whether to initialize layers immediately
            with_camera (bool): Whether to initialize camera immediately
        """
        self.title = title
        self.width = width
        self.height = height
        self.d_color = default_color
        # Store the real screen
        self._real_screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        
        self.clock = pg.time.Clock()
        self.running = True

        self.new_param = {}
        self.loop_phases = loop_phases or [lambda *a, **k: ...]
        self.white()
        self.key_map = {}
        if with_layers: self.init_layers()
        if with_camera: self.init_camera()
    
    # ! ================ CORE WINDOW METHODS ================
    def get_screen(self):
        """Get the main screen surface."""
        return self._real_screen

    def fill(self, color: tuple):
        """Fill the screen with a color."""
        self._real_screen.fill(color)

    def white(self):
        """Fill the screen with white color."""
        return self.get_active_surface().fill(self.d_color)

    def __update(self):
        """Update the display."""
        pg.display.update()

    def __tick(self, fps: int):
        """Control the frame rate."""
        self.clock.tick(fps)

    def quit(self):
        """Quit pygame."""
        pg.quit()

    # ! ================ GAME LOOP METHODS ================
    def heading(self, *layers_to_reset):
        """Handle events and prepare for the next frame."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        self.white()
        if not getattr(self, "_layers_initialized", False): 
            return
        for layer_name in layers_to_reset: 
            self.clear_layer(layer_name)

    def loop(self, *args, **kwargs):
        """Execute the game loop with all registered phases."""
        self.listen(*args, **kwargs)
        for step in self.loop_phases:
            step(*args, **kwargs, **self.new_param)

    def tailing(self, fps: int = 60):
        """
        Render all layers onto the main screen and update the display.
        If camera is active, renders the viewport portion of the camera surface.
        """
        if getattr(self, '_layers_initialized', False):
            for key, layer in self.layers.items():
                if self.layer_visibility[key]: 
                    self.get_active_surface().blit(layer, (0, 0))
        if getattr(self, '_camera_initialized', False) and self._camera_active:
            try:
                viewport_surface = self._camera_surface.subsurface(self.viewport_rect)
                scaled_viewport = pg.transform.scale(viewport_surface, (self.width, self.height))
                self._real_screen.blit(scaled_viewport, (0, 0))
            except ValueError:
                scaled_surface = pg.transform.scale(self._camera_surface, (self.width, self.height))
                self._real_screen.blit(scaled_surface, (0, 0))
        self.__update()
        self.__tick(fps)

    def add_loop_phase(self, lphase: Callable):
        """Add a new phase to the game loop."""
        self.loop_phases.append(lphase)

    def add_params(self, *_, **kwargs):
        """Add parameters to be passed to loop phases."""
        self.new_param.update(kwargs)

    # ! ================ INPUT HANDLING METHODS ================
    def add_key_map(self, key: int, func: Callable, *, once: bool = False):
        """
        Add an event listener for a key press.
        
        Args:
            key (int): The pygame key code to listen for
            func (Callable): The function to call when the key is pressed
            once (bool): If True, the function will only be called once per key press
                        If False, the function will be called continuously while the key is held
        """
        self.key_map[key] = [func, False, once]

    def add_multiple_key_map(self, *queries): 
        """Add multiple key mappings at once."""
        for query in queries: 
            if len(query) == 3: once = query[2]
            else: once = False
            self.add_key_map(query[0], query[1], once=once)

    def listen(self, *args, **kwargs): 
        """Process keyboard input and trigger registered callbacks."""
        keys = pg.key.get_pressed()
        for key, (func, being_called, once) in self.key_map.items():
            if keys[key]:
                if not once:
                    func(*args, **kwargs); continue
                if not being_called:
                    func(*args, **kwargs);
                    self.key_map[key][1] = True;
            else:
                self.key_map[key][1] = False

    # ! ================ LAYER SYSTEM METHODS ================
    def init_layers(self):
        """
        Initialize the layer system. Must be called before using any layer-related functions.
        Creates a dictionary to store layer surfaces and their visibility states.
        """
        self.layers: dict[Any, pg.Surface] = {}
        self.layer_visibility: dict[Any, bool] = {}
        self._layers_initialized = True

    def add_layer(self, key: Any, visible: bool = True) -> None:
        """
        Add a new layer with the specified key.
        Requires layers to be initialized first.
        
        Args:
            key: Unique identifier for the layer
            visible: Whether the layer should be visible by default
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions. "
                "You can also initialize layers during Window creation by setting with_layers=True"
            )
        self.layers[key] = pg.Surface((self.width, self.height), flags=pg.SRCALPHA)
        self.layers[key].fill((0, 0, 0, 0))
        self.layer_visibility[key] = visible

    def remove_layer(self, key: Any) -> None:
        """
        Remove a layer by its key.
        Requires layers to be initialized first.
        
        Args:
            key: The key of the layer to remove
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        if key in self.layers:
            del self.layers[key]
            del self.layer_visibility[key]

    def set_layer_visibility(self, key: Any, visible: bool) -> None:
        """
        Set the visibility of a layer.
        Requires layers to be initialized first.
        
        Args:
            key: The key of the layer to modify
            visible: Whether the layer should be visible
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        if key not in self.layers:
            raise KeyError(f"Layer with key '{key}' does not exist")
        self.layer_visibility[key] = visible

    def get_layer_visibility(self, key: Any) -> bool:
        """
        Get the visibility state of a layer.
        Requires layers to be initialized first.
        
        Args:
            key: The key of the layer to check
            
        Returns:
            bool: Whether the layer is visible
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        if key not in self.layers:
            raise KeyError(f"Layer with key '{key}' does not exist")
        return self.layer_visibility[key]

    def clear_layer(self, key: Any) -> None:
        """
        Clear the contents of a specific layer.
        Requires layers to be initialized first.
        
        Args:
            key: The key of the layer to clear
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        if key in self.layers:
            self.layers[key].fill((0, 0, 0, 0))

    def clear_all_layers(self) -> None:
        """
        Clear all layers.
        Requires layers to be initialized first.
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        for layer in self.layers.values():
            layer.fill((0, 0, 0, 0))

    def get_layer(self, key: Any) -> pg.Surface:
        """
        Get a layer surface by its key.
        Requires layers to be initialized first.
        
        Args:
            key: The key of the layer to get
            
        Returns:
            pygame.Surface: The requested layer surface
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        if key not in self.layers:
            raise KeyError(f"Layer with key '{key}' does not exist")
        return self.layers[key]

    def blit_in_layer(self, key: Any, *args, **kwargs) -> None:
        """
        Blit a surface onto a specific layer.
        Requires layers to be initialized first.
        
        Args:
            key: The key of the target layer
            surface: The surface to blit
            pos: Position (x, y) where to blit the surface
        """
        if not getattr(self, '_layers_initialized', False):
            raise RuntimeError(
                "Layers not initialized. Call init_layers() before using layer functions."
            )
        if key not in self.layers:
            raise KeyError(f"Layer with key '{key}' does not exist")
        self.layers[key].blit(*args, **kwargs)

    # ! ================ CAMERA SYSTEM METHODS ================
    @property
    def viewport_rect(self) -> pg.Rect:
        """Get the current viewport rectangle."""
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        return self._viewport_rect

    @viewport_rect.setter
    def viewport_rect(self, value):
        """
        Set the viewport rectangle with bounds checking.
        Accepts various input formats:
        - tuple/list of 2 numbers: (x, y) for new topleft position
        - tuple/list of 4 numbers: (x, y, width, height) for new rect
        - pg.Rect: new rect
        - dict: {'x': x, 'y': y, 'width': w, 'height': h} or {'centerx': cx, 'centery': cy}
        - number: scale factor for current rect
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        if not self._camera_active:
            raise RuntimeError("Camera must be active to modify viewport")

        current = self._viewport_rect.copy()
        
        if isinstance(value, (tuple, list)):
            if len(value) == 2:
                new_rect = current.copy()
                new_rect.x, new_rect.y = value
            elif len(value) == 4:
                new_rect = pg.Rect(*value)
            else:
                raise ValueError("Tuple/list must contain 2 or 4 numbers")
                
        elif isinstance(value, pg.Rect):
            new_rect = value.copy()
            
        elif isinstance(value, dict):
            new_rect = current.copy()
            if 'x' in value and 'y' in value:
                new_rect.x = value['x']
                new_rect.y = value['y']
            if 'width' in value and 'height' in value:
                new_rect.width = value['width']
                new_rect.height = value['height']
            if 'centerx' in value and 'centery' in value:
                new_rect.centerx = value['centerx']
                new_rect.centery = value['centery']
                
        elif isinstance(value, (int, float)):
            new_rect = current.copy()
            new_rect.width = int(current.width * value)
            new_rect.height = int(current.height * value)
            new_rect.centerx = current.centerx
            new_rect.centery = current.centery
            
        else:
            raise ValueError("Invalid input type for viewport_rect")

        new_rect.width = min(new_rect.width, self._camera_surface.get_width())
        new_rect.height = min(new_rect.height, self._camera_surface.get_height())
        
        max_x = self._camera_surface.get_width() - new_rect.width
        max_y = self._camera_surface.get_height() - new_rect.height
        new_rect.x = max(0, min(new_rect.x, max_x))
        new_rect.y = max(0, min(new_rect.y, max_y))
        
        self._viewport_rect = new_rect

    def init_camera(self):
        """
        Initialize the camera system. Must be called before using any camera-related functions.
        Sets up default camera viewport and surface.
        """
        self._camera_surface = pg.Surface((self.width * 2, self.height * 2))
        self._viewport_rect = pg.Rect(
            self.width // 2,
            self.height // 2,
            self.width,
            self.height
        )
        self._camera_zoom = 1.0
        self._camera_active = False
        self._camera_initialized = True

    def activate_camera(self):
        """
        Activate the camera system. This will redirect all drawing operations to the camera surface.
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        self._camera_active = True

    def deactivate_camera(self):
        """
        Deactivate the camera system. This will redirect all drawing operations back to the real screen.
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        self._camera_active = False

    def infocus(self, rect: pg.Rect, all: bool = False) -> bool:
        """
        Check if a rectangle is in the camera's focus zone.
        
        Args:
            rect: The rectangle to check
            all: If True, checks if the entire rectangle is in focus
                 If False, checks if any part of the rectangle is in focus
                 
        Returns:
            bool: Whether the rectangle is in focus
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        if not self._camera_active:
            raise RuntimeError("Camera must be active to use infocus()")
            
        if all:
            return self._viewport_rect.contains(rect)
        return self._viewport_rect.colliderect(rect)

    def move_camera(self, x: float, y: float):
        """
        Move the camera viewport by the specified amount.
        
        Args:
            x: Pixels to move right (negative for left)
            y: Pixels to move down (negative for up)
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        if not self._camera_active:
            raise RuntimeError("Camera must be active to use move_camera()")
            
        self.viewport_rect = (self._viewport_rect.x + x, self._viewport_rect.y + y)

    def set_camera(self, x: float, y: float):
        """
        Set the camera viewport to the specified position.
        
        Args:
            x: X coordinate in the camera surface
            y: Y coordinate in the camera surface
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        if not self._camera_active:
            raise RuntimeError("Camera must be active to use set_camera()")
            
        self.viewport_rect = {'centerx': x, 'centery': y}

    def zoom_in(self, ratio: float):
        """
        Zoom in the camera view.
        
        Args:
            ratio: The zoom ratio (must be > 1)
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        if not self._camera_active:
            raise RuntimeError("Camera must be active to use zoom_in()")
            
        if ratio <= 1:
            raise ValueError("Zoom ratio must be greater than 1")
            
        self._camera_zoom *= ratio
        self._update_viewport_size()

    def zoom_out(self, ratio: float):
        """
        Zoom out the camera view.
        
        Args:
            ratio: The zoom ratio (must be > 1)
        """
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        if not self._camera_active:
            raise RuntimeError("Camera must be active to use zoom_out()")
            
        if ratio <= 1:
            raise ValueError("Zoom ratio must be greater than 1")
            
        self._camera_zoom /= ratio
        self._update_viewport_size()

    def _update_viewport_size(self):
        """Update the viewport size based on the current zoom level."""
        if not getattr(self, '_camera_initialized', False):
            raise RuntimeError(
                "Camera not initialized. Call init_camera() before using camera functions."
            )
        
        self.viewport_rect = 1.0 / self._camera_zoom

    def get_active_surface(self):
        """
        Get the currently active surface for drawing.
        Returns the camera surface if camera is active, otherwise returns the real screen.
        """
        if getattr(self, '_camera_initialized', False) and self._camera_active:
            return self._camera_surface
        return self._real_screen

    def get_camera_transform(self, x: float, y: float) -> tuple[float, float]:
        """
        Transform world coordinates to screen coordinates using current camera viewport.
        This method is kept for backward compatibility but now returns the input coordinates
        since the camera system handles transformations differently.
        """
        return x, y

    # ! ================ DRAWING METHODS ================
    @dispatch(...)
    def blit(self, any: Any, *args, **kwargs):
        """Generic blit method that tries to use the object's __blit__ method."""
        try: 
            any.__blit__(*args, **kwargs)
        except AttributeError as e: 
            print(e)

    @dispatch(pg.Surface, object)
    def blit(self, surface: pg.Surface, pos: tuple, *, use_camera: bool = True):
        """Blit a surface onto the active surface."""
        target_surface = self.get_active_surface()
        x, y = pos
        target_surface.blit(surface, (x - surface.get_width()/2, y - surface.get_height()/2))

    @dispatch(AnimationSet, object)
    def blit(self, surface: AnimationSet, pos: tuple|pg.Rect, *, state=None, use_camera: bool = True):
        """Blit an animation set onto the active surface."""
        target_surface = self.get_active_surface()
        x, y = pos
        target_surface.blit(surface.generate(state), (x - surface.get_width()/2, y - surface.get_height()/2))

    @dispatch(Board)
    def blit(self, surface: Board, *,
            limits: bool = False, color=(0, 0, 0),
            line_width=2, overflow: bool = True, use_camera: bool = True):
        """Blit a board onto the active surface."""
        target_surface = self.get_active_surface()
        
        # Draw cells
        for i in range(surface.row):
            for j in range(surface.column):
                rect, color_ = surface.get_cell(i, j)
                surf = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
                surf.fill(color_)
                target_surface.blit(surf, rect)
        
        # Draw pieces
        for piece in surface.pieces:
            surface.draw_piece(self, piece, overflow=overflow)

        if not limits: return

        # Draw grid lines
        for i in range(surface.row + 1):
            level = surface.top + i*surface.cell_height
            pg.draw.line(target_surface, color, 
                    (surface.left, level),
                    (surface.right, level),
                    line_width)
        
        for j in range(surface.column + 1):
            level = surface.left + j*surface.cell_width
            pg.draw.line(target_surface, color, 
                    (level, surface.top),
                    (level, surface.bottom), 
                    line_width)

    def __getattribute__(self, name):
        """Special method to handle attribute access and delegation to active surface."""
        try:
            attr = super().__getattribute__(name)
            return attr
        except AttributeError:
            try: 
                attr = getattr(self._real_screen, name)
                return attr 
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


