
# Car class represents a vehicle in the simulation
class Car:
    def __init__(self, id, location):
        """
        Initialize a Car object.
        id: Unique identifier for the car
        location: Tuple (x, y) representing the car's position
        status: Current status of the car (e.g., 'available', 'en_route_to_pickup', etc.)
        assigned_rider: Rider object currently assigned to this car (None if not assigned)
        """
        self.id = id
        self.location = location
        self.status = "available"
        self.assigned_rider = None
