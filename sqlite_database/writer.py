import sqlite3
import json
import numpy as np
import io
"""This module initializes the SQLite database writer file for the Lunar Base simulation."""


# Define a function to save an environment element into the database
# This function takes a database connection and an element object as arguments
def save_environment_element(conn, element):
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Execute an SQL query to insert or replace the element into the environment_objects table
    cursor.execute("""
        INSERT OR REPLACE INTO environment_objects 
        (id, tag, class_name, x, y, length, width, radius, center)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        element.element_id,  # Unique identifier for the element
        getattr(element, 'tag', ''),  # Optional tag attribute
        element.__class__.__name__,  # Class name of the element
        getattr(element, 'x_coord', None),  # X-coordinate of the element
        getattr(element, 'y_coord', None),  # Y-coordinate of the element
        getattr(element, 'length', None),  # Length of the element (if applicable)
        getattr(element, 'width', None),  # Width of the element (if applicable)
        getattr(element, 'radius', None),  # Radius of the element (if applicable)
        json.dumps(getattr(element, 'center', {'x': None, 'y': None}))  # Center of the element with x and y values
    ))
    # Create another table to store each class's attributes and methods with their definitions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_definitions (
            class_name TEXT PRIMARY KEY,
            attributes TEXT,
            methods TEXT
        )
    """)
    
    # Prepare data for the class_definitions table
    attributes = ', '.join([attr for attr in dir(element) if not callable(getattr(element, attr)) and not attr.startswith("__")])
    methods = ', '.join([method for method in dir(element) if callable(getattr(element, method)) and not method.startswith("__")])
    
    # Insert or replace the class definition into the class_definitions table
    cursor.execute("""
        INSERT OR REPLACE INTO class_definitions 
        (class_name, attributes, methods)
        VALUES (?, ?, ?)
    """, (
        element.__class__.__name__,  # Class name of the element
        attributes,  # Comma-separated list of attributes
        methods  # Comma-separated list of methods
    ))
    conn.commit()
    # defined a function to save the final map of the internal robot tracks
def save_internal_robot_tracks(conn, internal_robot_tracks):
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    final_map = internal_robot_tracks.final_map  # Get the final map from the internal robot tracks
    robot_id = internal_robot_tracks.element_id  # Get the robot ID from the internal robot tracks
    buffer = io.BytesIO()
    np.save(buffer, final_map)  # save as binary .npy format
    buffer.seek(0)
    blob = buffer.read()
    cursor.execute("""
        INSERT OR REPLACE INTO internal_robot_tracks (id, final_map)
        VALUES (?, ?)
    """, (robot_id, blob))
    print("Element saved successfully.")
    # Commit the transaction to save changes to the database
    conn.commit()

# Define a function to save the designation target points for the robots
def save_designation_target_points(closest_points):
    
    # Execute an SQL query to insert or replace the element into the environment_objects table
    conn = sqlite3.connect('data/lunar_base_sim.db')
    cursor = conn.cursor()
    # Insert or replace the closest points into the internal_robot_target_points table
    for i, point in enumerate(closest_points):
        cursor.execute("INSERT OR REPLACE INTO internal_robot_target_points (id, point) VALUES (?, ?)", (f"superadobe_{i+1}", json.dumps(point)))
    conn.commit()
    conn.close()
    print("Closest points saved to the database successfully.")