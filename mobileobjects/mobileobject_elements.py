import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from .mobileobject_base import MobileObjectElement # Import the base class `EnvironmentElement` from the `environment_base` module in the same package.
import pygame  # Import Pygame for rendering
from typing import List  # Import List type for type hinting
from sqlite_database.reader import get_internal_robot_track_map  # Import the function to get the internal robot track map from the database

class InternalRobotElement(MobileObjectElement):
    """
    Class representing an internal robot element in the lunar base simulation.
    Inherits from the MobileObjectElement class.
    """

    def __init__(self, element_id, tag, x_coord, y_coord, velocity, **kwargs):
        """
        Initialize the InternalRobotElement with the given parameters.

        Parameters:
        - tag (str): Unique identifier for the internal robot.
        - mobile_object_map (numpy.ndarray): Map of the internal robot's environment.
        - target_list (List[tuple]): List of target positions for the internal robot.
        - current_position (tuple): Current position of the internal robot.
        - path (List[tuple]): Planned path for the internal robot.
        - target_position (tuple): Target position for the internal robot.
        - current_status (str): Current status of the internal robot.
        """
        type= 'InternalRobot'

        # Initialize the base class with the given parameters
        super().__init__(element_id, tag, x_coord, y_coord, velocity, type, **kwargs)
        # Initialize the internal robot's map
        self.mobile_object_map = np.array(get_internal_robot_track_map('InternalRobotTrack_1'))
        self.icon = pygame.image.load('data/assets/internal_robot_icon.png')  # Load the robot icon image
        self.icon = pygame.transform.scale(self.icon, (32, 32))  # Scale the icon to a suitable size
       
    
    def render(self, screen, transform_coords, scale=2):
        """
        Render the internal robot track and its current position on the Pygame screen.
        - screen: Pygame surface to draw on
        - transform_coords: function (x_mm, y_mm) -> (x_px, y_px)
        - scale: mm-to-pixel scaling factor
        """

        # Draw the robot at its current position
        x_px, y_px = self.current_position[0] * 2, self.current_position[1] * 2

        # Calculate angle (optional, based on velocity or direction)
        if hasattr(self, "direction_angle"):
            rotated_icon = pygame.transform.rotate(self.icon, -self.direction_angle)
        else:
            rotated_icon = self.icon

        icon_rect = rotated_icon.get_rect(center=(x_px, y_px+25))
        screen.blit(rotated_icon, icon_rect)

