from sqlite_database.reader import get_internal_robot_track_map
import numpy as np
import json
import pathfinding.core.grid
import pathfinding.finder.a_star
import math
class MobileObjectElement:
    """Base class for mobile objects in the simulation."""
    """Base (super) class for all mobile objects: InternalRobot,ExternalRobot,HumanTransportVehicle.
    Each mobile object subclass should inherit from this."""
    def __init__(self, element_id, tag, x_coord, y_coord, velocity, type, **kwargs):
        # Initialize the mobile object with a unique ID, name, and coordinates
        self.element_id = element_id  # Unique identifier for the element 
        self.tag= tag # Name of the mobile object
        self.x_coord = x_coord  # X-coordinate of the element's position
        self.y_coord = y_coord  # Y-coordinate of the element's position
        self.velocity = velocity  # Velocity of the mobile object
        # Store the current position of the mobile object
        self.current_position = (x_coord, y_coord)
        # Store the current position of the mobile object
        self.current_velocity = velocity
        # Store the current position of the mobile object
        self.current_status = "idle"
        # Store the target position of the mobile object
        self.target_position = None
        # Store the path of the mobile object
        self.path = None
        # Store the tasks of the mobile object
        self.tasks = None
        # Store the current task of the mobile object
        self.current_task = None
        # Store the current toolkit of the mobile object
        self.tool_kit = None
        # Store the targetlist of the mobile object
        self.target_list = []
        # Store the homelocation of the mobile object
        self.home_location = x_coord, y_coord
        # Store the map of the mobile object
        self.map = None
        # Store the tasktype of the mobile object
        self.task_type = []
        # Store the mobile object type
        self.mobile_object_type = type
        for key, value in kwargs.items():
            setattr(self, key, value)  # Dynamically set attributes for the object
    def __repr__(self):
        # Provide a string representation of the object for debugging and logging
        return f"<{self.__class__.__name__} - ID: {self.element_id}, Tag: {self.tag}>"
    

    def move(self):
        """
        Move the mobile object to the next position in the path based on mobile object velocity.
        This method updates the current position of the mobile object to the next position in the path.
        """
        # Check if the length of the path is greater than the current velocity step 
        if len(self.path) > self.current_velocity:
            # Update the current position of the mobile object to the next position in the path
            self.current_position = self.path[int(self.current_velocity)]
        else:
            # Update the current position of the mobile object to the last position in the path
            self.current_position = self.path[-1]
        # Print a message indicating that the mobile object is moving to the target position
        print(f"Mobile object {self.tag} is moving to target position {self.target_position}.")
        # Update the status of the mobile object to "moving"
        self.current_status = "moving"
    
    def path_planning(self):
        """
        Plan a path for the mobile object to reach the target position.
        
        Parameters:
        - target_position (tuple): Target position (x, y) for the mobile object.
        """
        """
        Plan a path for the mobile object to reach the target position.

        This method sets the target position, calculates the path using the
        pathfinding module, and updates the current status of the mobile object
        to "moving".

        Parameters:
        - target_position (tuple): Target position (x, y) for the mobile object.
        """
        # Create a grid based on the mobile object's map
        grid = pathfinding.core.grid.Grid(matrix=self.mobile_object_map)
        # Identify the start node from the current position
        start = grid.node(self.current_position[0], self.current_position[1])
        # Identify the end node from the target position
        end = grid.node(self.target_position[0], self.target_position[1])
        # Use the A* algorithm to find the path
        finder = pathfinding.finder.a_star.AStarFinder()
        path_temp, _ = finder.find_path(start, end, grid)
        # Convert the path to a list of (x, y) coordinates
        path = [(node.x, node.y) for node in path_temp]
        # Store the path in the object's attributes
        self.path = path
        # Update the status of the mobile object to "moving"
        self.current_status = "moving"
        self.update()
        # Print a message indicating that the path has been planned
        print(f"Path planned for mobile object {self.tag} to target position {self.target_position}.")

    def start(self):
        """
        Start the mobile object and set its status to "moving".
        """
        if self.target_list !=[]:
            # Set the target position to the first element in the target list
            self.target_position = self.target_list[0]
            # Remove the first element from the target list
            self.target_list.pop(0)
            self.current_task = self.tasks[0] # Set the current task to the first element in the tasks list
            # Plan the path to the target position
            self.path_planning()
            # Update the current position to the next position in the path
            self.update()
            print(f"Mobile object {self.tag} is moving to target position {self.target_position}.")
        else:
            print("No target position found.") 


    def update(self):

        """
        Update the position of the mobile object based on the planned path.
        
        This method checks if the mobile object is moving and updates its current position
        to the next position in the path. If the mobile object has reached the target position,
        it updates the current status to "idle" and prints a message indicating that the mobile object
        has reached the target position.
        Parameters:
        - none    
        """
        self.update_direction()
        if self.current_status == "moving":
            # Check if the mobile object has reached the target position
            if self.current_position == self.path[-1] and self.current_task != None:
                # Update the current status to "idle"
                self.current_status = "idle"
                #print(f"Mobile object {self.tag} has reached the target position {self.target_position}.")
                # Check if the mobile object has any target positions left
                if len(self.target_list) > 1:
                    # Set the target position to the next element in the target list
                    self.target_position = self.target_list[0]
                    # Plan the path to the target position
                    self.path_planning()
                else:
                    # Print a message indicating that the mobile object has no target positions left
                   # print(f"Mobile object {self.tag} has no target positions left, going to home location.")
                    # Set the target position to the home location
                    self.target_position = self.home_location
                    # Plan the path to the home location
                    self.path_planning() 
                    # Update the current task to None
                    self.current_task = None

            elif self.current_position == self.home_location and len(self.target_list) == 0 and self.current_task == None:
                # Print a message indicating that the mobile object has reached the home location
                #print(f"Mobile object {self.tag} has reached the home location {self.home_location}.")
                self.current_status = "idle"
                # Print current task completed
               # print(f"Mobile object {self.tag} has completed the current task.")
                # Remove the current task from the task list
                self.tasks.pop(0)
                
            else:
                # Update the current position to the next position in the path
                self.move()
                # Remove the first position from the path
                self.path.pop(0)
                # Print a message indicating that the mobile object is moving to the target position
                #print(f"Mobile object {self.tag} is moving to target position {self.target_position}.")
        elif self.current_status == "idle":
            # Print a message indicating that the mobile object is idle

            print(f"Mobile object {self.tag} is idle.")
        else:
            # Print a message indicating that the mobile object is not moving
            print(f"Mobile object {self.tag} is not moving.")
    
    def update_direction(self):
        self.direction_angle = 0
        if len(self.path) >= 2:
            dx = self.path[1][0] - self.path[0][0]
            dy = self.path[1][1] - self.path[0][1]
            angle_rad = math.atan2(dy, dx)
            self.direction_angle = math.degrees(angle_rad)
            

    def render(self):
        """
        Render the mobile object in the simulation.
        
        This method is a placeholder for rendering the mobile object in the simulation.
        It can be overridden by subclasses to provide specific rendering behavior.
        """
        pass