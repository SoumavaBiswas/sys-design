from ParkingLotDesign.parkingSpot import ParkingSpot
from ParkingLotDesign.vehicle import VehicleType
from typing import List

class ParkingFloor:
    def __init__(self, name: str, spot_size: int, vehicle_type: VehicleType):
        self.name = name
        self.spots = []
        for i in range(spot_size):
            self.spots.append(ParkingSpot(i, vehicle_type))
    
    def park(self, vehicle):
        for spot in self.spots:
            if spot.park(vehicle):
                return True
        return False    
    
    def unPark(self, vehicle):
        for spot in self.spots:
            if spot.unPark(vehicle):
                return True
        return False
    
    def display_availability(self):
        count = 0
        for spot in self.spots:
            if spot.isAvailable():
                count += 1
        return {self.name: count}