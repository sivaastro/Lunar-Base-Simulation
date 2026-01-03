import numpy as np
from scipy.spatial.distance import cdist

class Fire:
    """
    Fire event modeling analytical fire behavior in an environment.
    """

    def __init__(self, t0, t1MW, tlo, td, t_end, tg, loc, T_ignition, influence_radius, cooling_rate):
        """
        Initialize a fire event at a specific location.

        Parameters:
        - t0: Ignition onset time
        - t1MW: Time to reach 1 MW
        - tlo: Level-off time
        - td: Time q_dot reaches q_max
        - t_end: End time
        - tg: Growth time constant
        - loc: (x, y) tuple for fire location
        - T_ignition: Ignition temperature
        - influence_radius: Radius of heating effect
        - cooling_rate: Cooling constant
        """
        self.suppressed= False  # Suppression status
        self.t0 = t0
        self.t1MW = t1MW
        self.tlo = tlo
        self.td = td
        self.t_end = t_end
        self.tg = tg

        self.loc = loc  # (x, y)

        self.q_max = 1000 * ((self.tlo - self.t0) / (self.t1MW - self.t0)) ** 2
        self.alpha_d = self.q_max / (self.t_end - self.td) ** 2
        self.alpha_g = 1000 / (self.t1MW - self.t0) ** 2

        self.q = 0
        self.q_history = []
        self.T = 0  # Temperature
        self.Location_T = 0  # Temperature at fire location
        self.T_L = []  # History of local temp
        self.Status = "off"
        self.LocalT = 0

        self.cp = 1870  # Specific heat J/kgK
        self.mass = 100  # Initial mass kg
        self.m_r = self.mass  # Remaining mass
        self.c_r = self.mass / (self.t_end - self.t0)  # Consumption rate kg/s
        self.T_i = T_ignition
        self.k = cooling_rate
        self.influence_radius = influence_radius

        self.ambT = 25  # Ambient temp

        self.Tm = 1  # Mass loss time

    def update(self, location_system):
        """
        Update the fire behavior and surrounding environment.
        location_system should provide Temp() and Fire() methods.
        """
        temp_map = location_system.Temp()
        fire_map = location_system.Fire()

        self.Location_T = temp_map[self.loc[1], self.loc[0]]

        if (self.Location_T > self.T_i+10) and (self.m_r > 0):
            self.Status = "on"
            self.LocalT += 1   
            fire_map[self.loc[1], self.loc[0]] = 1
            location_system.Fire(fire_map)
            if self.LocalT <= self.t0:
                self.q = 0
            elif self.t0 < self.LocalT <= self.tlo:
                self._growth_I(self.LocalT)
            elif self.tlo < self.LocalT <= self.td:
                self._growth_II()
            elif self.td < self.LocalT <= self.t_end:
                self._decay(self.LocalT)
                if self.q==0:
                    self._mass_consumption(self.LocalT)
                
            else:
                self.q = 0
                fire_map[self.loc[1], self.loc[0]] = 0
                self.Status = "off"
                location_system.Fire(fire_map)

            if self.q > 0:
                fire_map[self.loc[1], self.loc[0]] = 1
                location_system.Fire(fire_map)
                self._mass_consumption(self.LocalT)
       
        
        

        else:
           
            self.q = 0
            self.Status = "off"
            fire_map[self.loc[1], self.loc[0]] = 0
            
            
        
        self._temperature_update(self.LocalT, location_system)
        self._surrounding_temperature(location_system)
        self.q_history.append(self.q)

    # ===== Private methods below =====
    
    def _growth_I(self, t):
        self.q = self.alpha_g * (t - self.t0) ** 2

    def _growth_II(self):
        self.q = self.alpha_g * (self.tlo - self.t0) ** 2

    def _decay(self, t):
        self.q = self.alpha_d * (self.t_end - t) ** 2

    def _mass_consumption(self, t):
         if t <= self.t_end:
           self.m_r = max(self.mass - (self.c_r * (t - self.t0)), 0)
         else:
           self.m_r = 0
        

    def _temperature_update(self, t, location_system):
        temp_map = location_system.Temp()

        if self.m_r > 0:
            self.T = 9.1 * (0.7 * self.q / 1000) ** (2 / 3) * (temp_map.mean() / (9.81 * 1.225 ** 2 * self.cp ** 2)) ** (1 / 3)
        else:
            self.T = 0

        if t >= self.td and self.Location_T > temp_map.mean() and self.m_r==0:
            self.Location_T = 25 + (self.Location_T - 25) * np.exp(-self.k * t)
        else:
            self.Location_T += self.T

        self.T_L.append(self.Location_T)
        temp_map[self.loc[1], self.loc[0]] = self.Location_T
        location_system.Temp(temp_map)

    def _surrounding_temperature(self, location_system):
        temp_map = location_system.Temp()
        y_indices, x_indices = np.nonzero(temp_map > 0)

        points = np.stack((x_indices, y_indices), axis=-1)
        fire_point = np.array([self.loc])

        distances = cdist(points, fire_point)

        affected = distances.flatten() < self.influence_radius

        for idx in np.where(affected)[0]:
            d = distances[idx][0]
            if d > 0:
                tx, ty = points[idx]
                temp_map[ty, tx] += (self.T * 0.7) / (d ** 2)

                # Clamp minimum to ambient
                if temp_map[ty, tx] < temp_map.mean():
                    temp_map[ty, tx] = temp_map.mean()

        location_system.Temp(temp_map)

    # ===== Public Fire Suppression method =====
    
    def fire_killing(self, n, suppression_type, location_system,extinguish_radius):
        """
        Apply external firefighting effort to reduce fire strength.
        
        Parameters:
        - n: Suppression factor
        - suppression_type: Type of suppression (currently unused)
        - location_system: environment model

        """
      
        self.Location_T -= (9.1 * (0.7 * n * 30) ** (2 / 3) * (location_system.Temp().mean() / (9.81 * 1.225 ** 2 * self.cp ** 2)) ** (1 / 3))

        if self.Location_T < 25:
            self.Location_T = 25
            self.Status = 'off'
            fire_map = location_system.Fire()
            fire_map[self.loc[1], self.loc[0]] = 0
            location_system.Fire(fire_map)

       # self.q -= (n * 1000)

        if self.q < 0:
            self.q = 0
            fire_map = location_system.Fire()
            fire_map[self.loc[1], self.loc[0]] = 0
            self.Status = 'off'
           
            location_system.Fire(fire_map)

        #self.q_history[-1] = self.q

        # Suppress surrounding temperatures
        temp_map = location_system.Temp()
        y_indices, x_indices = np.nonzero(temp_map > 0)
        points = np.stack((x_indices, y_indices), axis=-1)
        fire_point = np.array([self.loc])

        distances = cdist(points, fire_point)

        affected = distances.flatten() < (extinguish_radius)

        for idx in np.where(affected)[0]:
            tx, ty = points[idx]
            temp_map[ty, tx] -= (9.1 * (0.7 * n * 30) ** (2 / 3) * (location_system.Temp().mean() / (9.81 * 1.225 ** 2 * self.cp ** 2)) ** (1 / 3))

            if temp_map[ty, tx] < 25:
                temp_map[ty, tx] = 25
        
        location_system.Temp(temp_map)
       
