import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import neat
from location_system import Location
from fire_experiment import FireExperiment
from neat_fire_simulation import extract_sensor_input

# --- Load the trained NEAT winner ---
with open('best_robot_controller_7.pkl', 'rb') as f:
    winner = pickle.load(f)
MAX_FIRE_COUNT = 1  # Maximum number of fires to consider
GRID_SIZE = (13, 13)  # Grid size for the environment
SENSOR_RANGE = 2  # Sensor range for the robots
# --- Load NEAT configuration ---
config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(winner, config)

# --- Recreate the environment ---
experiment = FireExperiment(GRID_SIZE, max_steps=800)
experiment.deploy_materials()
experiment.ignite_random_material(MAX_FIRE_COUNT)

robots = []
for _ in range(5):
    x = np.random.randint(0, GRID_SIZE[1])
    y = np.random.randint(0, GRID_SIZE[0])
    robots.append({"pos": (x, y)})

# --- Simulation loop ---
for step in range(800):
        fire_positions = np.argwhere(Location.Fire() == 1)
        if len(fire_positions) == 0:
            break

        for robot in robots:
            robot_x, robot_y = robot["pos"]
            input_data = [robot_x / GRID_SIZE[1], robot_y / GRID_SIZE[0]]

            # Add fire positions (padded to 5)
            fire_inputs = []
            for idx in range(5):
                if idx < len(fire_positions):
                    fy, fx = fire_positions[idx]
                    dx = abs(fx - robot_x) / GRID_SIZE[1]
                    dy = abs(fy - robot_y) / GRID_SIZE[0]
                    fire_inputs.extend([dx, dy])
                else:
                    fire_inputs.extend([0.0, 0.0])
            input_data.extend(fire_inputs)

            # Add sensor input
            sensor_data = extract_sensor_input((robot_x, robot_y), GRID_SIZE, SENSOR_RANGE)
            input_data.extend(sensor_data)

            # Get NN decision
            output = net.activate(input_data)
            move_dir = np.argmax(output[:4])
            try_extinguish = output[4]
            print(f"Robot {robot} move_dir: {move_dir}")
            # Move robot
            if move_dir == 0 and robot_y > 0: 
                robot_y -= 1
            elif move_dir == 1 and robot_y < GRID_SIZE[0] - 1: 
                robot_y += 1
            elif move_dir == 2 and robot_x > 0: 
                robot_x -= 1
            elif move_dir == 3 and robot_x < GRID_SIZE[1] - 1: 
                robot_x += 1
            else:
                # If stuck near the edge, move towards the nearest fire
                if len(fire_positions) > 0:
                    nearest_fire = min(fire_positions, key=lambda f: abs(f[1] - robot_x) + abs(f[0] - robot_y))
                    fire_y, fire_x = nearest_fire
                    if robot_x < fire_x: 
                        robot_x += 1
                    elif robot_x > fire_x: 
                        robot_x -= 1
                    if robot_y < fire_y: 
                        robot_y += 1
                    elif robot_y > fire_y: 
                        robot_y -= 1

            robot["pos"] = (robot_x, robot_y)
            print(f"exteniguish: {try_extinguish}")
            # Try extinguishing
            if try_extinguish > 0.5:
                experiment.extinguish_fire((robot_x, robot_y), extinguish_radius=3, power=2.0)
            # Update fire state
            experiment.update_all()
            experiment.visualize([r["pos"] for r in robots])
            plt.pause(0.1)