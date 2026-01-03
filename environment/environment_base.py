class EnvironmentElement:
    """
    Base (super) class for all environment elements.
    Each environment subclass should inherit from this.
    """
    def __init__(self, element_id, tag, x_coord, y_coord, **kwargs):
        # Initialize the environment element with a unique ID, name, and coordinates
        self.element_id = element_id  # Unique identifier for the element
        self.tag= tag # Name of the environment element
        self.x_coord = x_coord  # X-coordinate of the element's position
        self.y_coord = y_coord  # Y-coordinate of the element's position
        
        # Store any additional attributes passed as keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)  # Dynamically set attributes for the object

    def __repr__(self):
        # Provide a string representation of the object for debugging and logging
        return f"<{self.__class__.__name__} - ID: {self.element_id}, Tag: {self.tag}>"
    
    
     
    
