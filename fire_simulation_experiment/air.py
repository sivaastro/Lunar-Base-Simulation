import numpy as np
class AirCooling:
    """
    AirCooling class to simulate the cooling effect on temperature at a given location.
    This class implements an exponential decay cooling model based on the current temperature.
    Attributes:
    - loc: Location of the cooling event (x, y) coordinates.
    - K: Cooling constant for the exponential decay.
    - time: Time step for the cooling effect.
    - temp: Current local temperature at the location.
    Methods:
    - update(location_system): Update the cooling effect based on the current temperature.
    - Cooling(location_system): Perform cooling based on the exponential decay formula.
    """
    def __init__(self, loc, cooling_constant=-0.013):
        """
        Initialize AirCooling event at a location with given cooling constant.
        """
        self.loc = loc  # (x, y) coordinate tuple
        self.K = cooling_constant  # Cooling constant
        self.time = 1  # Initialize time
        self.temp = None  # Current local temperature

    def update(self, location_system):
        """
        Update the cooling effect based on the current temperature.
        
        Parameters:
        - location_system: The external system that provides Temp() and Fire() states.
        """
        temp_map = location_system.Temp()
        fire_map = location_system.Fire()

        # If there's a fire at this location, don't cool
        if fire_map[self.loc[1], self.loc[0]] == 1:  # Note: row, col = (y, x) in numpy
            return

        self.temp = temp_map[self.loc[1], self.loc[0]]
        
        # Only cool if temperature > mean of all locations
        if self.temp > temp_map.mean():
            self.Cooling(location_system)
        else:
            return

    def Cooling(self, location_system):
        """
        Perform cooling based on exponential decay formula.
        """
        temp_map = location_system.Temp()

        # Cooling model: T = 25 + (T0 - 25) * exp(K * time)
        self.temp = 25 + (self.temp - 25) * np.exp(self.K * self.time)

        if self.temp < 25:
            self.temp = 25  # Clamp to 25 minimum

        # Update the global temperature map
        temp_map[self.loc[1], self.loc[0]] = self.temp
        location_system.Temp(temp_map)  # Save updated temp

        # Increment time
        self.time += 1
