import sqlite3
"""This module initializes the SQLite database schema for the Lunar Base simulation."""

def initialize_schema():
    """
    Initialize the SQLite database schema for the Lunar Base simulation.
    This function creates the necessary tables for storing environment objects and internal rover tracks.
    Args:
        db_path (str): Path to the SQLite database file. Defaults to 'lunar_base_sim.db'.
    """
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('data/lunar_base_sim.db')
    # Create a cursor object to interact with the database
    c = conn.cursor()

    # Create a table for storing environment objects
    c.execute('''
        CREATE TABLE IF NOT EXISTS environment_objects (
            id TEXT PRIMARY KEY,
            tag TEXT,
            class_name TEXT,
            x REAL,
            y REAL,
            length REAL,
            width REAL,
            radius REAL,
            center TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create a table for storing internal robots tracks including the final map value
    c.execute('''
        CREATE TABLE IF NOT EXISTS internal_robot_tracks (
            id TEXT PRIMARY KEY,
            final_map TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("Database schema initialized successfully.")

    # Execute an SQL query to insert or replace the element into the environment_objects table
   
    c.execute("CREATE TABLE IF NOT EXISTS  internal_robot_target_points (id TEXT PRIMARY KEY, point TEXT)")
    conn.commit()
    conn.close()