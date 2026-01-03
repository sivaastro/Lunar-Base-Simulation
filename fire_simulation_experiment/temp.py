import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import neat

from location_system import Location
from fire_experiment import FireExperiment
from neat_fire_simulation import extract_sensor_input

# --- Load the trained NEAT winner ---
with open('best_robot_controller_4.pkl', 'rb') as f:
    winner = pickle.load(f)
MAX_FIRE_COUNT = 5  # Maximum number of fires to consider
# --- Load NEAT configuration ---
config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(winner, config)

# --- Recreate the environment ---
experiment = FireExperiment(grid_size=(30, 30), max_steps=800)
experiment.deploy_materials()
experiment.ignite_random_material(MAX_FIRE_COUNT)

# --- Initialize multiple robots ---
n_robots = 5  # Number of robots
robot_positions = [ [np.random.randint(0, experiment.grid_size[1]),
                     np.random.randint(0, experiment.grid_size[0])]
                   for _ in range(n_robots)]

# --- Simulation loop ---
for step in range(experiment.max_steps):
    fire_positions = np.argwhere(Location.Fire() == 1)

    for idx, robot_position in enumerate(robot_positions):
        robot_x, robot_y = robot_position

        input_data = []
        input_data.append(robot_x / experiment.grid_size[1])
        input_data.append(robot_y / experiment.grid_size[0])
                

                # Relative positions to fires (pad if less fires)
        fire_inputs = []
        for idx in range(MAX_FIRE_COUNT):
            if idx < len(fire_positions):
                fy, fx = fire_positions[idx]
                dx = abs(fx - robot_x) / experiment.grid_size[1]
                dy = abs(fy - robot_y) / experiment.grid_size[0]
                fire_inputs.append(dx)
                fire_inputs.append(dy)
            else:
                # Pad with zeros if fewer fires
                fire_inputs.append(0.0)
                fire_inputs.append(0.0)

        input_data.extend(fire_inputs)

        sensor_data = extract_sensor_input((robot_x, robot_y), experiment.grid_size, 2)
        input_data.extend(sensor_data)
        
        # 2. Neural network output (only extinguish decision is used now)
        output = net.activate(input_data)
        
        move_dir = int(np.argmax(np.abs(output)))  # Use absolute values for movement decision
        try_extinguish = output[1]          # Last output is for extinguishing

        # 3. Move robot based on move_dir
        if move_dir == 0:    # Up
            robot_y = max(robot_y - 1, 0)
        elif move_dir == 1:  # Down
            robot_y = min(robot_y + 1, experiment.grid_size[0] - 1)
        elif move_dir == 2:  # Left
            robot_x = max(robot_x - 1, 0)
        elif move_dir == 3:  # Right
            robot_x = min(robot_x + 1, experiment.grid_size[1] - 1)

        # Update robot position
        robot_positions[idx] = [robot_x, robot_y]

        # 4. Extinguish fire if network output says so
        if try_extinguish > 0.5:
            experiment.extinguish_fire((robot_x, robot_y), extinguish_radius=2, power=1.0)

    # 5. Update fire spreading
    experiment.update_all()

    # 6. Visualize current environment and robots
    experiment.visualize(robot_positions=robot_positions)
