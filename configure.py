import numpy as np
from sqlite_database.reader import get_internal_robot_track_map, get_all_environment_elements
import sqlite3
import json
import heapq
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pandas as pd
# Connect to the SQLite database
import matplotlib.pyplot as plt
# Fetch all environment elements from the database
all_elements = get_all_environment_elements()
# Initialize a dictionary to store center values
center = {}

# Print the details of the superadobes (habitat structures)
for element in all_elements:
    # Convert all_elements to a pandas DataFrame
    all_elements_df = pd.DataFrame(all_elements)

    # Filter rows where classname is 'Superadobe'
    superadobes = all_elements_df[all_elements_df['class_name'] == 'Superadobe']

    # Print the details of the superadobes
    for _, row in superadobes.iterrows():
        center = json.loads(row.get('center', '{}'))
        print(f"Superadobe ID: {row.get('id')}, Center: {center}")
    
# Fetch the internal robot tracks from the database
# Load the final map for the internal robot with ID "IR01"
final_map_json = get_internal_robot_track_map("InternalRobotTrack_1")
# Convert the final map to a NumPy array
# Find the start and end points where the final map has a value of 1
start_point = None
end_point = None

points = [(j, i) for i, row in enumerate(final_map_json) for j, val in enumerate(row) if val == 1]
start_point, end_point = points[0], points[-1] if points else (None, None)

# Convert the final map to a NumPy array
global_map = np.array(final_map_json)

# Use the pathfinding library to find the shortest path
if start_point and end_point:
    grid = Grid(matrix=global_map)
    start = grid.node(*start_point)
    end = grid.node(*end_point)
    finder = AStarFinder()
    path, _ = finder.find_path(start, end, grid)
else:
    print("Start or end point not found in the map.")
global_map = np.array(final_map_json)
# Display the final map and path using matplotlib
if start_point and end_point and path:
    plt.figure(figsize=(10, 10))
    plt.imshow(global_map, cmap='gray')
    path_x, path_y = zip(*path)
    print(f"Path coordinates x: {path_x}, Path coordinates y: {path_y}")
    plt.plot(path_x, path_y, color='red', linewidth=2, label='Shortest Path')
    plt.scatter(*zip(*[start_point, end_point]), color='blue', label='Start/End Points')
    plt.colorbar()
    plt.title("Final Map with Shortest Path")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.show()
else:
    print("Cannot display path as it was not found.")
