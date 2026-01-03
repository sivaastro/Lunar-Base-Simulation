import numpy as np
"""Location class to manage the environment state for fire simulation.
This class provides methods to get and set the temperature and fire state of the environment.
Attributes:
- _temp: 2D numpy array representing the temperature at each location.
- _fire: 2D numpy array representing the fire state at each location (1 for fire, 0 for no fire).
Methods:
- Temp(new_temp=None): Get or set the temperature array.
- Fire(new_fire=None): Get or set the fire state array.
- initialize(grid_size=(100, 100)): Initialize or reset the location system with a specific grid size.
"""
class Location:
    _temp = None  # Temperature map (numpy array)
    _fire = None  # Fire map (numpy array)

    @classmethod
    def initialize(cls, grid_size):
        """
        Initialize or reset the location system with a specific grid size.
        - grid_size: (rows, cols) tuple
        """
        cls._temp = np.full(grid_size, 25.0)  # Default temperature 25°C
        cls._fire = np.zeros(grid_size)       # No fires initially
       

    @classmethod
    def Temp(cls, new_temp=None):
        """
        Get or set the temperature map.
        - new_temp: optional numpy array to replace current temperature map
        """
        if new_temp is not None:
            cls._temp = new_temp
        return cls._temp

    @classmethod
    def Fire(cls, new_fire=None):
        """
        Get or set the fire map.
        - new_fire: optional numpy array to replace current fire map
        """
        if new_fire is not None:
            cls._fire = new_fire
        return cls._fire
