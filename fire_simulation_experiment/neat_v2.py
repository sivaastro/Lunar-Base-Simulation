import neat
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from fire_experiment import FireExperiment
from location_system import Location
import random
TOTAL_MATERIALS = 10
GRID_SIZE = (30, 30)
NUM_ROBOTS = 5
SENSOR_RANGE = 2  # 5x5 grid
MOVE_PENALTY = 0.3
FIRE_REACHED_REWARD = 0.02
FIRE_EXTENGISH_REWARD= 5.0
SIM_TIME =300
extinguish_radius= 5
MAX_FIRE_COUNT = 5  # Maximum number of fires to extinguish
FIRE_CONSTRAINT_TIME=100
STUCK_PANELTY = +0.005  # Penalty for being stuck in the same position
def get_local_grid(center, robot_positions):
    cx, cy = center
    temp = Location.Temp() / 100.0

    grid = np.zeros((2 * SENSOR_RANGE + 1, 2 * SENSOR_RANGE + 1))

    for dy in range(-SENSOR_RANGE, SENSOR_RANGE + 1):
        for dx in range(-SENSOR_RANGE, SENSOR_RANGE + 1):
            x, y = cx + dx, cy + dy
            gx, gy = dx + SENSOR_RANGE, dy + SENSOR_RANGE
            if 0 <= x < GRID_SIZE[1] and 0 <= y < GRID_SIZE[0]:
                if (x, y) in robot_positions:
                    grid[gy, gx] = -1  # Mark obstacle by -1
                else:
                    grid[gy, gx] = temp[y, x]
            else:
                grid[gy, gx] = 0  # Out of bounds as 0
    return grid.flatten()

def evaluate_genomes(genomes, config):
    def yx_to_xy(yx):
        """Convert (row, col) → (x, y) format."""
        y, x = yx
        return (x, y)
     
    for genome_id, genome in genomes:
        random_seed = 42
        np.random.seed(random_seed)
        random.seed(random_seed)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        experiment = FireExperiment(grid_size=GRID_SIZE, max_steps=800)
        experiment.deploy_materials(TOTAL_MATERIALS)
        experiment.ignite_random_material(MAX_FIRE_COUNT)
        Stuck_panelty = 0
        robots = []
        move_panelty = 0
        for _ in range(NUM_ROBOTS):
            x = np.random.randint(0, GRID_SIZE[1])
            y = np.random.randint(0, GRID_SIZE[0])
            robots.append({"pos": (x, y), "stagnation_counter": 0})
        team_fitness = 0


       # plt.close()
        
        for step in range(SIM_TIME):
            temp_grid = Location.Temp() / 100.0
            fire_grid = Location.Fire()
            robot_positions = [robot["pos"] for robot in robots]

            for i, robot in enumerate(robots):
                robot_x, robot_y = robot["pos"]
                input_data = get_local_grid((robot_x, robot_y), robot_positions=robot_positions)
                output = net.activate(input_data)
                move_dir = int(np.argmax(output[:4]))
                
                old_pos = (robot_x, robot_y)

                # Define movement directions: [up, down, left, right]
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
                # else: keep old position if move is invalid
                

                robot["pos"] = (robot_x, robot_y)

                # Temperature-based fitness update
                if old_pos != robot["pos"]:
                    prev_temp = temp_grid[old_pos[1], old_pos[0]]
                    curr_temp = temp_grid[robot_y, robot_x]
                    temp_gain = (curr_temp - prev_temp) / temp_grid.max()

                    if temp_gain < 0:
                                team_fitness -= MOVE_PENALTY / SIM_TIME
                                k=1
                    else:
                                team_fitness += MOVE_PENALTY / SIM_TIME
                                k=-1
                    move_panelty += k*MOVE_PENALTY / SIM_TIME
                # Stagnation penalty
               
                   
                    # If robot is stagnant, check if near fire; if so, reduce stagnation_counter
                if old_pos == robot["pos"]:
                    fire_locations = np.argwhere(fire_grid > 0)  # (y, x)
                    near_fire = any(
                        np.linalg.norm(np.array((x_fire, y_fire)) - np.array(robot["pos"])) <= extinguish_radius
                        for y_fire, x_fire in fire_locations
                    )
                    if near_fire:
                        robot["stagnation_counter"] = max(0, robot["stagnation_counter"] - 1)
                        team_fitness += FIRE_REACHED_REWARD / SIM_TIME
                        experiment.extinguish_fire(robot["pos"], extinguish_radius, power=1.0)
                    else:
                        robot["stagnation_counter"] += 1
                        team_fitness -= STUCK_PANELTY / SIM_TIME
                        Stuck_panelty += STUCK_PANELTY / SIM_TIME
            
            #experiment.visualize(robot_positions=robot_positions)
            
                       
                      
                       


                
            stagnation_counter = sum(robot["stagnation_counter"] for robot in robots)
               

            # Fire reduction fitness
            

            experiment.update_all()
            
            

            
          
            # End conditions
            if np.sum(fire_grid) == 0:
                print(f"All fires extinguished! Genome {genome_id} and step time: {step}")
                team_fitness +=FIRE_CONSTRAINT_TIME/step
                break
            if stagnation_counter >=10:
               # print(f"Robots stagnated for too long! Genome {genome_id} and step time: {step}")
                
               
                break
        
        genome.fitness = team_fitness  # Normalize fitness by number of robots
        print(f"Genome {genome_id} fitness: {genome.fitness:.4f}, Stagnation: {stagnation_counter}, Stuck penalty: {Stuck_panelty}, Move penalty: {move_panelty:.4f}")
        # Check robot stagnation
        
       

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

    winner = p.run(evaluate_genomes, 100)

    with open('best_robot_controller_9.pkl', 'wb') as f:
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



if __name__ == "__main__":
    run_neat('config-feedforward')
