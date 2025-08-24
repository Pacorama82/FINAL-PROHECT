
import heapq
from car import Car
from rider import Rider

TRAVEL_SPEED_FACTOR = 1


# Simulation class manages the event-driven simulation engine
class Simulation:
    def __init__(self):
        """
        Initialize the simulation with event queue, time, cars, and riders.
        """
        self.event_heap = []  # Min-heap for scheduling events
        self.current_time = 0 # Simulation clock
        self.cars = {}        # Dictionary of Car objects
        self.riders = {}      # Dictionary of Rider objects


    def run(self):
        """
        Main event loop: processes events in chronological order until the queue is empty.
        Pops the next event, advances the clock, and calls the appropriate handler.
        """
        while self.event_heap:
            timestamp, event_type, data = heapq.heappop(self.event_heap)
            self.current_time = timestamp
            if event_type == "RIDER_REQUEST":
                self.handle_rider_request(data)
            elif event_type == "ARRIVAL":
                self.handle_arrival(data)


    def find_closest_car_brute_force(self, rider_location):
        """
        Finds the closest available car to the given rider location using brute-force search.
        Returns the Car object with the minimum Manhattan distance.
        """
        min_dist = float('inf')
        closest_car = None
        for car in self.cars.values():
            if car.status == "available":
                dist = abs(car.location[0] - rider_location[0]) + abs(car.location[1] - rider_location[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_car = car
        return closest_car


    def calculate_travel_time(self, start_location, end_location):
        """
        Calculates travel time between two locations using Manhattan distance and a speed factor.
        """
        distance = abs(start_location[0] - end_location[0]) + abs(start_location[1] - end_location[1])
        return distance * TRAVEL_SPEED_FACTOR


    def handle_rider_request(self, rider):
        """
        Handles a new rider request event:
        - Finds the closest available car
        - Links car and rider, updates statuses
        - Schedules pickup arrival event
        - Logs the dispatch action
        """
        car = self.find_closest_car_brute_force(rider.start_location)
        if car:
            car.assigned_rider = rider
            car.status = "en_route_to_pickup"
            pickup_duration = self.calculate_travel_time(car.location, rider.start_location)
            heapq.heappush(self.event_heap, (self.current_time + pickup_duration, "ARRIVAL", car))
            print(f"TIME {self.current_time}: CAR {car.id} dispatched to RIDER {rider.id}")


    def handle_arrival(self, car):
        """
        Handles an arrival event for a car:
        - If picking up, updates location/statuses and schedules dropoff
        - If dropping off, updates location/statuses and frees the car
        - Logs each event
        """
        rider = car.assigned_rider
        if car.status == "en_route_to_pickup":
            print(f"TIME {self.current_time}: CAR {car.id} picked up RIDER {rider.id}")
            car.location = rider.start_location
            car.status = "en_route_to_destination"
            rider.status = "in_car"
            dropoff_duration = self.calculate_travel_time(rider.start_location, rider.destination)
            heapq.heappush(self.event_heap, (self.current_time + dropoff_duration, "ARRIVAL", car))
        elif car.status == "en_route_to_destination":
            print(f"TIME {self.current_time}: CAR {car.id} dropped off RIDER {rider.id}")
            car.location = rider.destination
            car.status = "available"
            rider.status = "completed"
            car.assigned_rider = None

# --- DEMO ---

sim = Simulation()
sim.cars[1] = Car(1, (0, 0))
sim.cars[2] = Car(2, (10, 10))
sim.riders[1] = Rider(1, (2, 3), (5, 5))
sim.riders[2] = Rider(2, (8, 9), (0, 0))

# Schedule initial rider requests
heapq.heappush(sim.event_heap, (0, "RIDER_REQUEST", sim.riders[1]))
heapq.heappush(sim.event_heap, (1, "RIDER_REQUEST", sim.riders[2]))

sim.run()