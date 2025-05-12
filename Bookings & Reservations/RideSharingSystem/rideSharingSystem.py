import uuid
from enum import Enum

class User:
    def __init__(self, username, location):
        self.id = str(uuid.uuid4())[:6]
        self.username = username
        self.location = location
        self.ride_history = []


class Driver(User):
    def __init__(self, username, location, vehicle):
        super().__init__(username, location)
        self.vehicle = vehicle
        self.is_available = True


class Rider(User):
    def __init__(self, username, location):
        super().__init__(username, location)


class Location:
    def __init__(self, lattitude, longitude):
        self.lattitude = lattitude
        self.longitude = longitude
    
    def distance_to(self, other):
        dx = self.latitude - other.latitude
        dy = self.longitude - other.longitude
        return (dx ** 2 + dy ** 2) ** 0.5


class RideStatus(Enum):
    REQUESTED = "Requested"
    CONFIRMED = "Confirmed"
    STARTED = "Started"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Ride:
    def __init__(self, rider: Rider, origin:Location, destination:Location):
        self.id = str(uuid.uuid4())[:6]
        self.rider = rider
        self.driver = None
        self.origin = origin
        self.destination = destination
        self.status = RideStatus.REQUESTED
        self.fare = 0
    
    def assign_driver(self, driver:Driver):
        self.driver = driver
        self.driver.is_available = False

    def start_ride(self):
        self.status = RideStatus.STARTED
    
    def end_ride(self):
        self.status = RideStatus.COMPLETED
        self.fare = self.calculate_price()
        self.rider.ride_history.append(self)
        self.driver.ride_history.append(self)
        self.is_available = True
    
    def calculate_price(self):
        return self.origin.distance_to(self.destination) * 10
    
    def get_fare(self):
        return self.fare


class RideSharingSystem:
    def __init__(self):
        self.active_rides = []
    
    def request_ride(self, user, origin, destination):
        ride = Ride(user, origin, destination)
        self.active_rides.append(ride)
        return ride

    def match_driver(self, ride:Ride, nearby_drivers):
        for driver in nearby_drivers:
            if driver.is_available:
                ride.assign_driver(driver)
                return ride
        return None

class DriverLocationServices:
    def __init__(self):
        self.driver_location = {}

    def update_location(self, driver_id, location):
        self.driver_location[driver_id] = location
    
    def get_nearby_drivers(self, rider_location:Location, radius_km=5):
        nearby_drivers = []
        for driver, location in self.driver_location:
            if rider_location.distance_to(location) <= radius_km:
                nearby_drivers.append(driver)
        return nearby_drivers


