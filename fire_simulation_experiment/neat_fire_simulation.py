import neat
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from fire_experiment import FireExperiment
from location_system import Location

GRID_SIZE = (30, 30)
NUM_ROBOTS = 5
SENSOR_RANGE = 2

def extract_sensor_input(robot_pos, grid_size, sensor_range):
    x, y = robot_pos
    x = max(0, min(x, grid_size[1] - 1))
    y = max(0, min(y, grid_size[0] - 1))

    temp_grid = Location.Temp()
    padded_grid = np.pad(temp_grid, sensor_range, mode='constant', constant_values=0)
    x_p, y_p = x + sensor_range, y + sensor_range
    sensor_area = padded_grid[y_p - sensor_range:y_p + sensor_range + 1,
                              x_p - sensor_range:x_p + sensor_range + 1]
    
    assert sensor_area.shape == (2 * sensor_range + 1, 2 * sensor_range + 1), \
        f"Sensor grid shape invalid: {sensor_area.shape} at {robot_pos}"
    return sensor_area.flatten() / 100.0

def evaluate_genomes(genomes, config):
    # Updated rewards/penalties
    DISTANCE_WEIGHT = -0.3
    OVERLAP_PENALTY = -1.0
    MOVE_PENALTY = -0.05
    COORDINATION_REWARD = 1.0
    EXTINGUISH_REWARD = 5.0
    TIME_BONUS = 2.0
    MAX_FIRE_COUNT = 5
    CLUSTER_RADIUS = 5

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        experiment = FireExperiment(grid_size=GRID_SIZE, max_steps=800)
        experiment.deploy_materials()
        experiment.ignite_random_material(size=3)

        robots = []
        for _ in range(NUM_ROBOTS):
            x = np.random.randint(0, GRID_SIZE[1])
            y = np.random.randint(0, GRID_SIZE[0])
            robots.append({"pos": (x, y)})

        team_fitness = 0

        for step in range(800):
            fire_positions = np.argwhere(Location.Fire() == 1)
            prev_fire_count = len(fire_positions)
            if prev_fire_count == 0:
                break

            for robot in robots:
                robot_x, robot_y = robot["pos"]

                input_data = [robot_x / GRID_SIZE[1], robot_y / GRID_SIZE[0]]

                fire_inputs = []
                for idx in range(MAX_FIRE_COUNT):
                    if idx < len(fire_positions):
                        fy, fx = fire_positions[idx]
                        dx = (fx - robot_x) / GRID_SIZE[1]
                        dy = (fy - robot_y) / GRID_SIZE[0]
                        fire_inputs.extend([dx, dy])
                    else:
                        fire_inputs.extend([0.0, 0.0])
                input_data.extend(fire_inputs)

                sensor_data = extract_sensor_input((robot_x, robot_y), GRID_SIZE, SENSOR_RANGE)
                input_data.extend(sensor_data)

                output = net.activate(input_data)

                move_dir = int(np.argmax(output[:4]))
                try_extinguish = output[4]

                # Move robot
                old_pos = (robot_x, robot_y)
                if move_dir == 0 and robot_y > 0:
                    robot_y -= 1
                elif move_dir == 1 and robot_y < GRID_SIZE[0] - 1:
                    robot_y += 1
                elif move_dir == 2 and robot_x > 0:
                    robot_x -= 1
                elif move_dir == 3 and robot_x < GRID_SIZE[1] - 1:
                    robot_x += 1
                else:
                    # If stuck at the edges, move towards the nearest fire
                    if fire_positions.size > 0:
                        nearest_fire = min(fire_positions, key=lambda f: np.linalg.norm(np.array(f) - np.array((robot_y, robot_x))))
                        fy, fx = nearest_fire
                        if robot_x < fx:
                            robot_x += 1
                        elif robot_x > fx:
                            robot_x -= 1
                        if robot_y < fy:
                            robot_y += 1
                        elif robot_y > fy:
                            robot_y -= 1
                robot["pos"] = (robot_x, robot_y)

                if robot["pos"] != old_pos:
                    team_fitness += MOVE_PENALTY

                experiment.update_all()

                if try_extinguish > 0.5:
                    experiment.extinguish_fire((robot_x, robot_y), extinguish_radius=3, power=2.0)

            # Team fitness evaluation
            fire_positions = np.argwhere(Location.Fire() == 1)
            for (fy, fx) in fire_positions:
                for robot in robots:
                    rx, ry = robot["pos"]
                    dist = np.linalg.norm(np.array((fx, fy)) - np.array((rx, ry))) / max(GRID_SIZE)
                    team_fitness += DISTANCE_WEIGHT * dist

            # Penalize overlapping
            robot_positions = [robot["pos"] for robot in robots]
            unique_positions = set(robot_positions)
            overlaps = len(robot_positions) - len(unique_positions)
            if overlaps > 0:
                team_fitness += OVERLAP_PENALTY * overlaps

            # Reward clustering near fire
            for (fy, fx) in fire_positions:
                near_robots = 0
                for robot in robots:
                    rx, ry = robot["pos"]
                    if np.linalg.norm(np.array((fx, fy)) - np.array((rx, ry))) <= CLUSTER_RADIUS:
                        near_robots += 1
                if near_robots > 1:
                    team_fitness += COORDINATION_REWARD * (near_robots / NUM_ROBOTS)

            fire_count = np.count_nonzero(Location.Fire())
            if fire_count < prev_fire_count:
                extinguished = prev_fire_count - fire_count
                team_fitness += EXTINGUISH_REWARD * extinguished

            if fire_count == 0:
                team_fitness += (300 - step - 1) * TIME_BONUS
                break
            # print(f'move_dir: {move_dir}, try_extinguish: {try_extinguish}')
        print(f"Genome {genome_id} fitness: {team_fitness/1700}")
        genome.fitness = team_fitness/1700

def run_neat(config_filename):
    config_path = os.path.join(os.path.dirname(__file__), config_filename)
    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(evaluate_genomes, 50)

    with open('best_robot_controller_7.pkl', 'wb') as f:
        pickle.dump(winner, f)

    plot_stats(stats, view=True)

def plot_stats(statistics, ylog=False, view=False, filename='fitness.svg'):
    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]

    plt.plot(generation, best_fitness, label="best")
    plt.title("Best fitness over generations")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    if view:
        plt.show()

def simulate_best_controller(pickle_file='best_robot_controller.pkl', config_file='config-feedforward'):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    with open(pickle_file, 'rb') as f:
        best_genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    experiment = FireExperiment(grid_size=GRID_SIZE, max_steps=800)
    experiment.deploy_materials()
    experiment.ignite_random_material(size=3)

    robots = []
    for _ in range(NUM_ROBOTS):
        x = np.random.randint(0, GRID_SIZE[1])
        y = np.random.randint(0, GRID_SIZE[0])
        robots.append({"pos": (x, y)})

    for step in range(800):
        fire_positions = np.argwhere(Location.Fire() == 1)
        if len(fire_positions) == 0:
            break

        for robot in robots:
            robot_x, robot_y = robot["pos"]
            input_data = [robot_x / GRID_SIZE[1], robot_y / GRID_SIZE[0]]

            fire_inputs = []
            for idx in range(5):
                if idx < len(fire_positions):
                    fy, fx = fire_positions[idx]
                    dx = (fx - robot_x) / GRID_SIZE[1]
                    dy = (fy - robot_y) / GRID_SIZE[0]
                    fire_inputs.extend([dx, dy])
                else:
                    fire_inputs.extend([0.0, 0.0])

            input_data.extend(fire_inputs)
            sensor_data = extract_sensor_input((robot_x, robot_y), GRID_SIZE, SENSOR_RANGE)
            input_data.extend(sensor_data)

            output = net.activate(input_data)
            move_dir = int(np.argmax(output[:4]))
            try_extinguish = output[4]

            if move_dir == 0 and robot_y > 0: robot_y -= 1
            elif move_dir == 1 and robot_y < GRID_SIZE[0] - 1: robot_y += 1
            elif move_dir == 2 and robot_x > 0: robot_x -= 1
            elif move_dir == 3 and robot_x < GRID_SIZE[1] - 1: robot_x += 1

            robot["pos"] = (robot_x, robot_y)

            if try_extinguish > 0.5:
                experiment.extinguish_fire((robot_x, robot_y), extinguish_radius=3, power=2.0)

        if step % 5 == 0:  # More frequent visualization
            experiment.visualize([r["pos"] for r in robots])

    print("Simulation completed.")

if __name__ == "__main__":
    run_neat('config-feedforward')
