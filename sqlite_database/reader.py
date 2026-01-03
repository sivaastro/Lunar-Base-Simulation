import sqlite3
import json
import numpy as np
import io
import pandas as pd

"""
This module provides functions to interact with the lunar base simulation database.
"""

def get_all_environment_elements():
    db_path='data/lunar_base_sim.db'
    """
    Fetches all environment elements from the database and returns them as a pandas DataFrame.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        pandas.DataFrame: A DataFrame representation of all rows in the environment_objects table.
    """

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM environment_objects"
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

def get_internal_robot_track_map(track_id):

    db_path='data/lunar_base_sim.db'
    
    """
    Fetches a specific internal rover track by its ID from the database.

    Args:
        track_id (int): The ID of the rover track to fetch.
        db_path (str): Path to the SQLite database file.

    Returns:
        list: A list of tuples representing the rows in the internal_rover_tracks table with the specified ID.
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT final_map FROM internal_robot_tracks WHERE id = ?", (track_id,))
    row = cursor.fetchone()
    if row and row[0]:
        buffer = io.BytesIO(row[0])
        return np.load(buffer)

# Define a function to get the designation targets points for the robots
def get_designation_targets_points(superadobe_id):
    """
    Fetches only the first designation target point for the given superadobe ID from the database.

    Args:
        superadobe_id (str): The ID of the superadobe element.

    Returns:
        dict or None: A dictionary of the target point if found, otherwise None.
    """
    db_path = 'data/lunar_base_sim.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT point FROM internal_robot_target_points WHERE id = ? LIMIT 1", (superadobe_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None
