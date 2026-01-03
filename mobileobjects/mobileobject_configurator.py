from mobileobjects.mobileobject_elements import InternalRobotElement

def configure_internal_robot_element(points, **kwargs):
    """
    Configure an internal robot element with the given parameters.
    
    Parameters:
    - element_id (str): Unique identifier for the internal robot.
    - tag (str): Name of the internal robot.
    - x_coord (float): X-coordinate of the internal robot's position.
    - y_coord (float): Y-coordinate of the internal robot's position.
    - velocity (float): Velocity of the internal robot.
    - type (str): Type of the internal robot.
    - **kwargs: Additional keyword arguments for configuration.
    
    Returns:
    - InternalRobotElement: Configured internal robot element.
    """
    # Create and return an instance of InternalRobotElement with the provided parameters
    internal_robot_elements = []
    for i, (x_coord, y_coord) in enumerate(points, start=1):
        element_id = f'InternalRobot_{i}'
        tag = f'IR_{i}'
        velocity = 1.0
        internal_robot_elements.append(InternalRobotElement(element_id, tag, x_coord, y_coord, velocity, **kwargs))
    return internal_robot_elements
    
