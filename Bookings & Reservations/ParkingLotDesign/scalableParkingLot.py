from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import heapq

"""
1. Vehicle 
2. Parking Spot 
3. Ticket
4. ParkingLot
5. PaymentProcessor
"""


# -------------------- Vehicle Classes --------------------
class Vehicle(ABC):
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

class Bike(Vehicle):
    pass

class Car(Vehicle):
    pass

class Truck(Vehicle):
    pass

# -------------------- Parking Spot --------------------
class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: str, floor_number: int):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.floor_number = floor_number
        self.is_occupied = False
        self.vehicle = None

    def park_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_occupied = True

    def remove_vehicle(self):
        self.vehicle = None
        self.is_occupied = False

    def __lt__(self, other):  
        return self.floor_number < other.floor_number  

# -------------------- Ticket --------------------
class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None

    def close_ticket(self):
        self.exit_time = datetime.now()

# -------------------- Pricing Strategy --------------------
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, ticket: Ticket):
        pass

class HourlyPricing(PricingStrategy):
    def __init__(self, rate_per_hour: float):
        self.rate_per_hour = rate_per_hour

    def calculate_price(self, ticket: Ticket):
        duration = (datetime.now() - ticket.entry_time).seconds / 3600
        return round(duration * self.rate_per_hour, 2)

# -------------------- Payment Processor --------------------
class PaymentProcessor:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def process_payment(self, ticket: Ticket):
        return self.strategy.calculate_price(ticket)

# -------------------- Parking Lot --------------------
class ParkingLot:
    def __init__(self, name: str):
        self.name = name
        self.floors = {}
        self.available_spots = {}  # { vehicle_type: MinHeap of spots }
        self.occupied_spots = {}  # { ticket_id: (ticket, spot) }

    def add_floor(self, floor_number: int):
        self.floors[floor_number] = []

    def add_parking_spot(self, spot: ParkingSpot):
        if spot.spot_type not in self.available_spots:
            self.available_spots[spot.spot_type] = []
        heapq.heappush(self.available_spots[spot.spot_type], (spot.floor_number, spot))

    def park_vehicle(self, vehicle: Vehicle):
        vehicle_type = vehicle.__class__.__name__
        
        if vehicle_type not in self.available_spots or not self.available_spots[vehicle_type]:
            return None  # No available spot
        
        _, spot = heapq.heappop(self.available_spots[vehicle_type])  # Get the nearest available spot
        spot.park_vehicle(vehicle)
        ticket = Ticket(vehicle, spot)
        self.occupied_spots[ticket.ticket_id] = (ticket, spot)
        return ticket

    def exit_vehicle(self, ticket_id: str, payment_processor: PaymentProcessor):
        if ticket_id not in self.occupied_spots:
            return "Invalid Ticket"

        ticket, spot = self.occupied_spots.pop(ticket_id)
        ticket.close_ticket()
        price = payment_processor.process_payment(ticket)
        spot.remove_vehicle()
        heapq.heappush(self.available_spots[spot.spot_type], (spot.floor_number, spot))  # Re-add to available spots
        return f"Payment Due: {price}"

