
# Rider class represents a passenger in the simulation
class Rider:
    def __init__(self, id, start_location, destination):
        """
        Initialize a Rider object.
        id: Unique identifier for the rider
        start_location: Tuple (x, y) representing the rider's pickup location
        destination: Tuple (x, y) representing the rider's dropoff location
        status: Current status of the rider (e.g., 'waiting', 'in_car', 'completed')
        """
        self.id = id
        self.start_location = start_location
        self.destination = destination
        self.status = "waiting"
