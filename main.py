from environment.loader import load_environment_from_excel  # Import the function to load environment data from an Excel file
from environment.environment_elements import visualize_environment  # Import the function to visualize the environment
from simulation_visualizer.simulation_visualizer_element import SimulationVisualizer  # Import the SimulationVisualizer class for rendering the environment
from sqlite_database.schema import initialize_schema
from sqlite_database.writer import save_environment_element, save_internal_robot_tracks, save_designation_target_points
from sqlite_database.reader import get_designation_targets_points  # Import the function to get all environment elements from the database
import sqlite3  # Import the SQLite library for database operations
import json  # Import the JSON library for data serialization
import numpy as np  # Import NumPy for numerical operations
from mobileobjects.mobileobject_configurator import configure_internal_robot_element
"""
This module serves as the main entry point for the Lunar Base simulation.
It orchestrates the loading of environment data, visualization, and database operations.
It is responsible for initializing the database schema, loading environment elements from an Excel file,
visualizing the environment, and saving the elements to the database.
The main function is executed when the script is run directly.
It is designed to be modular and extensible, allowing for easy integration of new features and components.
"""

def main():
    # Load environment objects from the specified Excel file
    env_data = load_environment_from_excel()
   
    # Print out the details of the superadobes (habitat structures)
   
    all_elements = (
        env_data['Superadobes'] +
        env_data['PressurizedModules'] +
        env_data['SuperadobePaths'] +
        env_data['ControlTowers'] +
        env_data['PavedRoads'] +
        env_data['HumanQuitAreas'] +
        env_data['CommunicationCenters'] +
        env_data['LoadingDocks'] +
        env_data['LunarTransportationSheds']+
        env_data['ClearanceAreas']+
        env_data['InternalRobotTracks'] 
    )  # Combine all environment elements into a single list
    # Visualize the entire environment using the provided visualization function
  
   
    initialize_schema()  # Initialize the SQLite database schema
    # Store to database without waiting
    # visualize_environment(all_elements) 
    visualizer= SimulationVisualizer()  # Create an instance of the SimulationVisualizer class
    visualizer.render_static_environment(all_elements)  # Render the static environment elements onto a separate surface
   
    conn = sqlite3.connect('data/lunar_base_sim.db')
    storing_elements = [element for element in all_elements if element not in env_data['ClearanceAreas'] and element not in env_data['InternalRobotTracks']]
    for element in storing_elements:
        save_environment_element(conn, element)
    # Save the internal robot tracks to the database
    for track in env_data['InternalRobotTracks']:
        save_internal_robot_tracks(conn, track)
    
   # Extract superadobe center coordinates and store them in a np.array for accessibility
    superadobe_centers = [element.center for element in env_data['Superadobes']]
    superadobe_centers = np.array(superadobe_centers)*0.5
    # print(f"Superadobe centers: {superadobe_centers}")
    conn.close()  # Close the database connection
   
   # Extract the points from the final map of the internal robot tracks
    final_map = env_data['InternalRobotTracks'][0].final_map
    points = [(j, i) for i, row in enumerate(final_map) for j, val in enumerate(row) if val == 1]
   
   # Now find the closet point to the superadobe centers/2 on the points from the final map to save as a designation points for the robots for each superadobe
   # print(f"Points from the final map: {points}")
    if not points:
        print("No points found in the final map.")
        return
    # Find the closest point to the superadobe centers
    closest_points = [
        min(points, key=lambda p: np.linalg.norm(np.array(p) - np.array(center)))
        for center in superadobe_centers
    ]
    # print(f"Closest points for each superadobe center: {closest_points}")
    # Save the closest points to the database
    save_designation_target_points(closest_points)   
    
    #get the designation targets points for the robots
    designation_targets_points = []
    for superadobe_id in range(10, 14):  # Loop through superadobe IDs from 7 to 28 (inclusive)
        points = get_designation_targets_points(f'superadobe_{superadobe_id}')[:2]
        designation_targets_points.append(points)
    print(f"Designation targets points for the robots: {designation_targets_points}")
  
    # Configure the internal robot element with the loaded environment data
    internal_robot_elements = configure_internal_robot_element(designation_targets_points) 
    print(f"Internal robot elements: {internal_robot_elements}")
    internal_robot_elements[0].target_list = [tuple(internal_robot_elements[1].current_position)]
    internal_robot_elements[1].target_list = [tuple(internal_robot_elements[0].current_position)]
    internal_robot_elements[3].target_list = [tuple(internal_robot_elements[2].current_position)]
    internal_robot_elements[2].target_list = [tuple(internal_robot_elements[3].current_position)]
    # print the internal robot elements target position and target list
   
    for element in internal_robot_elements:
        element.tasks=[('testing')]
        element.start()
        
    print(f"Internal robot elements target position: {internal_robot_elements[0].target_position}")
    print(f"Internal robot elements target list: {internal_robot_elements[1].target_position}")
    # Start the internal robot elements
    # print the current task of the internal robot elements
    print(f"Internal robot elements current task: {internal_robot_elements[0].current_task}")
    # print the current status of the internal robot elements
    
    # Render the internal robot elements onto the main screen
    while True:
        # Draw only dynamic elements (robots)
        for element in internal_robot_elements:
            element.update()
        visualizer.render_frame(internal_robot_elements)  # Render the dynamic elements (robots) onto the main screen
    
    print("Simulation completed successfully.")  # Print a message indicating successful completion of the simulation
if __name__ == "__main__":
    main()  # Execute the main function when the script is run directly
