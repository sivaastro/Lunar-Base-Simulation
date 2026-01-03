import pickle
import neat
import numpy as np
from fire_experiment import FireExperiment
from location_system import Location
from neat_v2 import get_local_grid
import random
import os

# ==== Constants ====
TOTAL_MATERIALS = 10
GRID_SIZE = (30, 30)
NUM_ROBOTS = 5
SENSOR_RANGE = 2
MOVE_PENALTY = -0.03
FIRE_REACHED_REWARD = 2.0
SIM_TIME = 200
extinguish_radius = 5
MAX_FIRE_COUNT = 5
FIRE_CONSTRAINT_TIME = 100
STUCK_PENALTY = -5.0



def simulate_best_controller(controller_path, config_path):
    # Load genome and config
    with open(controller_path, 'rb') as f:
        genome = pickle.load(f)

    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Fixed environment
    random_seed = 42
    np.random.seed(random_seed)
    random.seed(random_seed)

    experiment = FireExperiment(grid_size=GRID_SIZE, max_steps=800)
    experiment.deploy_materials(TOTAL_MATERIALS)
    experiment.ignite_random_material(MAX_FIRE_COUNT)

    robots = []
    for _ in range(NUM_ROBOTS):
        x = np.random.randint(0, GRID_SIZE[1])
        y = np.random.randint(0, GRID_SIZE[0])
        robots.append({"pos": (x, y), "stagnation_counter": 0})

    team_fitness = 0

    for step in range(SIM_TIME):
        temp_grid = Location.Temp() / 100.0
        fire_grid = Location.Fire()
        robot_positions = [robot["pos"] for robot in robots]

        for i, robot in enumerate(robots):
            robot_x, robot_y = robot["pos"]
            input_data = get_local_grid((robot_x, robot_y), robot_positions=robot_positions)
            output = net.activate(input_data)
            move_dir = int(np.argmax(output[:4]))
           
           

            directions = [
                    (0, -1),  # up
                    (0, 1),   # down
                    (-1, 0),  # left
                    (1, 0)    # right
                ]
            dx, dy = directions[move_dir]
            new_x = robot_x + dx
            new_y = robot_y + dy

            # Check if new position is within grid bounds and not occupied
            if 0 <= new_x < GRID_SIZE[1] and 0 <= new_y < GRID_SIZE[0] and (new_x, new_y) not in robot_positions:
                robot_x, robot_y = new_x, new_y
           
            fire_locations = np.argwhere(fire_grid > 0)
            for y_fire, x_fire in fire_locations:
                fire_pos = (x_fire, y_fire)
                if np.linalg.norm(np.array(fire_pos) - np.array(robot["pos"])) <= extinguish_radius:
                    team_fitness += FIRE_REACHED_REWARD / SIM_TIME
                    experiment.extinguish_fire(robot["pos"], extinguish_radius, power=1.0)

       

        experiment.update_all()
        experiment.visualize(robot_positions=[r["pos"] for r in robots])

      
# Run the simulation
if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)  # directory of the current script
    config_path1 = os.path.join(current_dir, "config-feedforward")
    config_path2 = os.path.join(current_dir, "best_robot_controller_9.pkl")
    simulate_best_controller(config_path2, config_path1)
