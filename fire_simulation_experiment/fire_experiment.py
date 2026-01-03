import numpy as np
import matplotlib.pyplot as plt
from numpy import mean
from fire import Fire
from location_system import Location
from numpy.linalg import norm

class FireExperiment:
    def __init__(self, grid_size=(100, 200), max_steps=500):
        self.grid_size = grid_size
        self.max_steps = max_steps
        self.fires = []  # List of Fire instances
        self.coolers = []  # List of AirCooling instances
        self.step = 0
        Location.initialize(grid_size)  # Initialize the location system
        # Initialize environment
        Location._temp = np.full(self.grid_size, 25.0)
        Location._fire = np.zeros(self.grid_size)
     
    
    def deploy_materials(self,size):
        """
        Place materials as fire instances with different ignition temperatures.
        """
        materials = {
            "wood": 50,     # °C
            "plastic": 70,  # °C
            "metal": 40     # °C (almost never burns)
        }
       

        for _ in range(size): # 50 material points
            x = np.random.randint(0, self.grid_size[1])
            y = np.random.randint(0, self.grid_size[0])

            material_type = np.random.choice(list(materials.keys()))
            T_ignition = materials[material_type]

            fire = Fire(
                t0=10, t1MW=85, tlo=180, td=190, t_end=460, tg=30,
                loc=(x, y),
                T_ignition=T_ignition,
                influence_radius=8,
                cooling_rate=0.00001
            )
            
            self.fires.append(fire)

    def ignite_random_material(self,size=5):
        """
        Artificially heat some material points to start the fire.
        """
        fire_map = Location.Fire()
        for fire in np.random.choice(self.fires, size, replace=False):
            temp_map = Location.Temp()
            temp_map[fire.loc[1], fire.loc[0]] = fire.T_i + 50  # 20°C above ignition
           
            fire_map[fire.loc[1], fire.loc[0]] = 1
            Location.Fire(fire_map)
            Location.Temp(temp_map)


    def update_all(self):
        """
        Update all fires and air coolers.
        """
        fire_map = Location.Fire()
        for fire in self.fires:
            fire.update(Location)
        self.step += 1 
        
        Location.Fire(fire_map)
        self.passive_cooling_step()

        
    def visualize(self, robot_positions):
        """
        Update and visualize the environment:
        - Temperature map
        - Fire map
        - Fire material mass/status
        - Robot positions (updated cleanly)
        """
        temp = Location.Temp()
        fire_map = Location.Fire()
        fires = self.fires

        if not hasattr(self, '_fig'):
            # Create figure and axes
            self._fig, self._axs = plt.subplots(1, 3, figsize=(18, 6))

            # Temperature Map
            self._im1 = self._axs[0].imshow(temp, cmap='jet', vmin=20, vmax=np.max(temp))
            self._axs[0].set_title('Temperature Map')
            self._axs[0].set_xlabel('X-axis')
            self._axs[0].set_ylabel('Y-axis')
            plt.colorbar(self._im1, ax=self._axs[0])

            # Fire Map
            self._im2 = self._axs[1].imshow(fire_map, cmap='Reds')
            self._axs[1].set_title('Fire Map')
            self._axs[1].set_xlabel('X-axis')
            self._axs[1].set_ylabel('Y-axis')
            plt.colorbar(self._im2, ax=self._axs[1])

            # Fire Status Bar Chart
            material_labels = [f"M{i+1}" for i in range(len(fires))]
            self._bar = self._axs[2].bar(
                material_labels,
                [fire.m_r for fire in fires],
                color=['red' if fire.Status == "on" else 'blue' for fire in fires]
            )
            self._axs[2].set_title('Fire Material Mass')
            self._axs[2].set_xlabel('Material')
            self._axs[2].set_ylabel('Remaining Mass (kg)')
            self._axs[2].tick_params(axis='x', rotation=90)

            self._robot_markers = []  # << NEW: To keep track of plotted robots

            plt.suptitle(f"Step: {self.step}")
            plt.tight_layout()
            plt.ion()
            plt.show()

        else:
            # Update temperature and fire maps
            self._im1.set_data(temp)
            self._im1.set_clim(vmin=20, vmax=np.max(temp))

            self._im2.set_data(fire_map)

            # Update bar chart
            for bar, fire in zip(self._bar, fires):
                bar.set_height(fire.m_r)
                bar.set_color('red' if fire.Status == "on" else 'blue')

            self._fig.suptitle(f"Step: {self.step}")

            # === 🧹 Clear old robot markers
            for marker in getattr(self, '_robot_markers', []):
                marker.remove()
            self._robot_markers = []
            # === 🟩 Plot new robot positions
            for (x, y) in robot_positions:
                adjusted_y = self.grid_size[0] - y  # Adjust height to height - y
                marker, = self._axs[1].plot(x,y, marker='s', color='green', markersize=6, markeredgewidth=1)
                self._robot_markers.append(marker)
                

            self._fig.canvas.draw()
            self._fig.canvas.flush_events()

        plt.pause(0.1)


    def run(self, visualize_every=10):
        """
        Run the full fire propagation experiment.
        """
        self.deploy_materials()
        self.ignite_random_material()
    
        
        print("Starting simulation...")
        temp_map = Location.Temp()
        fire_map = Location.Fire()
        print(f"Initial temperature: {mean(temp_map)} °C")
        while np.max(temp_map) > 50.0:
            self.update_all()
            temp_map = Location.Temp()
            self.step += 1
            fire=self.fires
            # print which fire is on
            if self.step % visualize_every == 0:
                self.visualize()
            
        print("Simulation finished!")


    def passive_cooling_step(self):
        """
        Apply Newton's cooling across the entire temperature map.
        """
        temp = Location.Temp()
        ambient_temp = 25.0  # Room ambient temperature
        cooling_constant = 0.001  # Experiment with values

        # Newton's Law of Cooling:
        # dT/dt = -k * (T - T_ambient)
        temp = temp + cooling_constant * (ambient_temp - temp)

        Location.Temp(temp)
    

    def extinguish_fire(self, robot_position, extinguish_radius=5, power=5.0):
        """
        Extinguish fires near the robot's current position.
        
        Parameters:
        - robot_position: (x, y) tuple of robot location
        - extinguish_radius: maximum distance to affect fire
        - power: how strong the extinguisher is (1.0 = normal)
        """
        x, y = robot_position
  

        # Precomputed fire locations (N,2)
        for fire in self.fires:

            if fire.Status == "on":
                # Calculate distance from robot to fire
                dist = np.linalg.norm(np.array(fire.loc) - np.array((x, y)))
                if dist <= extinguish_radius:
                   # print(f"Extinguishing fire at {fire.loc} with power {power} from robot at {robot_position}")
                    fire.fire_killing(n=power, suppression_type='basic', location_system=Location, extinguish_radius=extinguish_radius)
