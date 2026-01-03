import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from .environment_base import EnvironmentElement # Import the base class `EnvironmentElement` from the `environment_base` module in the same package.
import pygame  # Import Pygame for rendering
from typing import List  # Import List type for type hinting

# Import the base class `EnvironmentElement` from the `environment_base` module in the same package.
class Superadobe(EnvironmentElement):
    """
    Represents a Superadobe structure (igloo-shaped) on the lunar base.
    Additional attributes may include radius, height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord,
                 radius=0.0, height=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.radius = radius
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(int(self.x_coord), int(self.y_coord))
        r_scaled = int(self.radius * scale)
        rect = pygame.Rect(x_px - r_scaled, y_px - r_scaled, 2 * r_scaled, 2 * r_scaled)
        pygame.draw.ellipse(screen, (0, 255, 0), rect, width=3)
        self.center = (x_px, y_px)  # Update center with transformed coordinates


class PressurizedModule(EnvironmentElement):
    """
    Represents a pressurized module (habitat) on the lunar base.
    Additional attributes: length, width, height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord,
                 length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (0, 169, 11), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates


class SuperadobePath(EnvironmentElement):
    """
    Represents a path between Superadobe path on the lunar base.
    Additional attributes: length, width, height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord,
                 length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (104, 255, 42), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates


class ControlTower(EnvironmentElement):
    """
    Represents a control tower on the lunar base.
    Additional attributes: height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord, length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (25, 255, 251), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates


class PavedRoad(EnvironmentElement):
    def __init__(self, element_id, tag, x_coord, y_coord, length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (25, 255, 251), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates


class CommunicationCenter(EnvironmentElement):
    """
    Represents a communication center on the lunar base.
    Additional attributes: height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord, radius=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.radius = radius
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        r_scaled = int(self.radius * scale)
        rect = pygame.Rect(x_px - r_scaled, y_px - r_scaled, 2 * r_scaled, 2 * r_scaled)
        pygame.draw.ellipse(screen, (0, 255, 0), rect, width=3)
        self.center = (x_px, y_px)  # Update center with transformed coordinates


class HumanQuitArea(EnvironmentElement):
    """
    Represents a human quit area on the lunar base.
    Additional attributes: height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord, length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (0, 169, 11), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates


class LoadingDock(EnvironmentElement):
    """
    Represents a loading dock on the lunar base.
    Additional attributes: height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord, length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (255, 255, 0), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates


class LunarTransportationShed(EnvironmentElement):
    """
    Represents a lunar transportation shed on the lunar base.
    Additional attributes: height, material, etc.
    """
    def __init__(self, element_id, tag, x_coord, y_coord, length=0.0, width=0.0, **kwargs):
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        self.length = length
        self.width = width
        self.center = None  # Center will be calculated during rendering

    def render(self, screen, transform_coords, scale):
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length * scale)
        w_px = int(self.width * scale)
        rect = pygame.Rect(x_px, y_px - w_px, l_px, w_px)
        pygame.draw.rect(screen, (255, 255, 0), rect, width=3)
        self.center = (x_px + l_px / 2, y_px - w_px / 2)  # Update center with transformed coordinates
        print("render is completed for LunarTransportationShed")
# Create a ClearanceArea class that inherits from EnvironmentElement
class ClearanceArea(EnvironmentElement):
    def __init__(self, element_id, tag, x_coord, y_coord, length=0.0, width=0.0, **kwargs):
        # Initialize the ClearanceArea object with its unique ID, tag, coordinates, and other optional attributes.
        super().__init__(element_id, tag, x_coord, y_coord, **kwargs)
        # Call the constructor of the parent class `EnvironmentElement` to initialize common attributes.
        self.length = length
        # Set the length of the clearance area.
        self.width = width
        # Set the width of the clearance area.
    def render(self, screen, transform_coords,scale):
        """
        Render the clearance area on a Pygame screen.   
        Parameters:
        screen (pygame.Surface): The surface to draw on.
        transform_coords (function): A function to convert real coordinates to screen pixels.#   font = pygame.font.SysFont('Arial', 12)
#    text_surf = font.render(self.tag, True, (255, 255, 255))
#    text_rect = text_surf.get_rect(center=(x_px, y_px))
 #       screen.blit(text_surf, text_rect)
        """
        x_px, y_px = transform_coords(self.x_coord, self.y_coord)
        l_px = int(self.length*scale)
        w_px = int(self.width*scale)
        rect = pygame.Rect(x_px,  y_px-w_px, l_px, w_px)
        pygame.draw.rect(screen, (0, 0, 0), rect)
        #   font = pygame.font.SysFont('Arial', 12)
#    text_surf = font.render(self.tag, True, (255, 255, 255))
#    text_rect = text_surf.get_rect(center=(x_px, y_px))
 #       screen.blit(text_surf, text_rect)
       

# Create a class InternalRobotTrack that inherits from EnvironmentElement
class InternalRobotTrack(EnvironmentElement):
    """
    Represents the internal rover's path as a visual line and rectangle overlay.
    """
    def __init__(self, element_id, tag, lines, rects, **kwargs):
        super().__init__(element_id, tag, 0, 0, **kwargs)
        self.lines = lines  # List of ((x1, y1), (x2, y2)) tuples
        self.rects = rects  # List of (x, y, w, h) tuples
        self.path = []  # List of points for the path
        self.map = None  # Without scaling for the map
        self.final_map = None  # Final map after scaling
        self.path_extracted = False  # Flag to ensure extract_path is called only once
        self.extract_path()  # Call the method to extract the path immediately upon initialization

    def render(self, screen, transform_coords, scale):
    #   Render the internal rover's path on the Pygame screen.
        print("render called for InternalRobotTrack")
        # Draw lines
        for (x1, y1), (x2, y2) in self.lines:
            pt1 = transform_coords(x1, y1)
            pt2 = transform_coords(x2, y2)
            pygame.draw.line(screen, (0, 0, 255), pt1, pt2, width=2)

        # Draw rectangles
        for x, y, w, h in self.rects:
            x_px, y_px = transform_coords(x, y)
            w_px = int(w * scale)
            h_px = int(h * scale)
            rect = pygame.Rect(x_px, y_px - h_px, w_px, h_px)
            pygame.draw.rect(screen, (0, 0, 255), rect, width=2)
       

       

    def extract_path(self):
        print("extract_path called")
        """Extract the path from the map and store it in the path attribute."""
        # Finalize rendering to an empty surface and store it in the map attribute
        pygame.init()
        # Get actual screen size (fullscreen resolution)
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        # Optional: Use full screen
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

        real_width_mm = 1571
        real_height_mm = 874

        scale_x = screen_width / real_width_mm
        scale_y =  screen_height/ real_height_mm
        scale = min(scale_x, scale_y)  # Preserve aspect ratio

        
        empty_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        empty_surface.fill((0, 0, 0, 0))  # Transparent background
        transform_coords_inter = lambda x_mm, y_mm: (int(x_mm * scale), int(screen_height - y_mm * scale))
        # Draw lines and rectangles on the empty surface
        for (x1, y1), (x2, y2) in self.lines:
            pt1 = transform_coords_inter(x1, y1)
            pt2 = transform_coords_inter(x2, y2)
            pygame.draw.line(empty_surface, (0, 0, 255), pt1, pt2, width=3)

        for x, y, w, h in self.rects:
            x_px, y_px = transform_coords_inter(x, y)
            w_px = int(w * scale)
            h_px = int(h * scale)
            rect = pygame.Rect(x_px, y_px - h_px, w_px, h_px)
            pygame.draw.rect(empty_surface, (0, 0, 255), rect, width=3)
        
        # Store the rendered map
        self.map = empty_surface

        # Extract the path from the map and store it in the path attribute by resizing the map into 25% of its original size
        if self.map:
            # Convert the map to a binary image
            resized_map = pygame.transform.scale(self.map, (self.map.get_width() // 2, self.map.get_height() //2))
            # Store the final map after scaling
            resized_map_array = pygame.surfarray.array_alpha(resized_map)
            pygame.quit()
            # Convert the numpy array to a binary image
            resized_map_array = np.where(resized_map_array > 0, 1, 0)
            # rotate the map by 90 degrees
            resized_map_array = np.rot90(resized_map_array)
            # Store the resized map in the final_map attribute
            self.final_map = resized_map_array
            print("Path extracted successfully.")
        else:
            print("Map is empty. Cannot extract path.")




def visualize_environment(elements: List['EnvironmentElement']):
    pygame.init()
   # Get actual screen size (fullscreen resolution)
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    # Optional: Use full screen
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Lunar Base Environment")
    clock = pygame.time.Clock()

    real_width_mm = 1571
    real_height_mm = 874

    scale_x = screen_width / real_width_mm
    scale_y =  screen_height/ real_height_mm
    scale = min(scale_x, scale_y)  # Preserve aspect ratio

    def transform_coords(x_mm, y_mm):
        """Transform mm to pixel coordinates, flip Y for screen space"""
        x_px = int(x_mm * scale)
        y_px = int(screen_height - y_mm * scale)
        return x_px, y_px

    # Fill the screen with a black background
    screen.fill((0, 0, 0))  # Black background

    # Render each element in the environment
    for element in elements:
        element.render(screen, transform_coords, scale)
        # Print a message indicating that the element rendering is completed
        print(f"Rendering completed for element: {element.tag}")

    # Update the display with the rendered content
    pygame.display.flip()

    print("Rendering completed for all elements.")
    pygame.quit()

