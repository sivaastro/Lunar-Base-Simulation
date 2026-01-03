import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import neat

from location_system import Location
from fire_experiment import FireExperiment
TOTAL_MATERIALS = 20  # Total number of materials to deploy
MAX_FIRE_COUNT =16
GRID_SIZE = (100, 100)
experiment = FireExperiment(GRID_SIZE, max_steps=800)
experiment.deploy_materials(TOTAL_MATERIALS)
experiment.ignite_random_material(MAX_FIRE_COUNT)
NUM_ROBOTS = 5
robots = []
extinguish_radius=2
for _ in range(NUM_ROBOTS):
    x = np.random.randint(0, GRID_SIZE[1])
    y = np.random.randint(0, GRID_SIZE[0])
    robots.append({"pos": (x, y)})

team_fitness = 0

for step in range(800):
    temp_grid = Location.Temp() / 100.0
    fire_grid = Location.Fire()
    robot_positions = [robot["pos"] for robot in robots]

    for i, robot in enumerate(robots):
        robot_x, robot_y = robot["pos"]
        # Move robot randomly: up, down, left, or right (stay within grid)
        # Find all fire locations
        fire_locations = np.argwhere(fire_grid > 0)

        if len(fire_locations) > 0:
            # Flip (y, x) → (x, y) during unpacking
            distances = [np.linalg.norm([x_fire - robot_x, y_fire - robot_y]) 
                        for y_fire, x_fire in fire_locations]
            
            nearest_idx = np.argmin(distances)
            y_fire, x_fire = fire_locations[nearest_idx]
            dist_to_fire = distances[nearest_idx]
            
            print(f"Robot {i} at {robot['pos']} moving towards fire at {(x_fire, y_fire)} with distance {dist_to_fire}")

            if dist_to_fire <= extinguish_radius:
                robot["pos"] = (robot_x, robot_y)
            else:
                dx = np.sign(x_fire - robot_x)
                dy = np.sign(y_fire - robot_y)
                new_x = max(0, min(GRID_SIZE[1] - 1, robot_x + dx))
                new_y = max(0, min(GRID_SIZE[0] - 1, robot_y + dy))

                # Check if another robot is within 1 radius of the new position
                too_close = False
                for j, other_robot in enumerate(robots):
                    if i == j:
                        continue
                    ox, oy = other_robot["pos"]
                    if np.linalg.norm([ox - new_x, oy - new_y]) < 1.1:
                        too_close = True
                        break
                if too_close:
                    # Try alternative adjacent positions closer to the fire
                    alternatives = [
                        (max(0, min(GRID_SIZE[1] - 1, robot_x + dx)), robot_y),
                        (robot_x, max(0, min(GRID_SIZE[0] - 1, robot_y + dy))),
                        (max(0, min(GRID_SIZE[1] - 1, robot_x + dx)), max(0, min(GRID_SIZE[0] - 1, robot_y))),
                        (robot_x, robot_y)
                    ]
                    # Sort alternatives by distance to fire
                    alternatives = sorted(alternatives, key=lambda pos: np.linalg.norm([x_fire - pos[0], y_fire - pos[1]]))
                    for alt_x, alt_y in alternatives:
                        if all(np.linalg.norm([other_robot["pos"][0] - alt_x, other_robot["pos"][1] - alt_y]) >= 1.1 for j, other_robot in enumerate(robots) if i != j):
                            new_x, new_y = alt_x, alt_y
                            break
                robot["pos"] = (new_x, new_y)
        experiment.extinguish_fire(robot["pos"], extinguish_radius, power=1.0)
    
    # all fires are extenguished, then stop the experiment
    if np.sum(fire_grid) == 0:
        print("All fires extinguished!")
        break
   

    experiment.update_all()
    
    
    experiment.visualize(robot_positions=robot_positions)


