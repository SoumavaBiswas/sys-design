from typing import List
from ParkingLotDesign.parkingFloor import ParkingFloor

class ParkingLot:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ParkingLot, cls).__new__(cls)
            cls._instance.floors = []
        return cls._instance
    
    def add_parking_floor(self, floor: ParkingFloor):
        self.floors.append(floor)
    
    def park(self, vehicle):
        for floor in self.floors:
            if floor.park(vehicle):
                return True
        return False

    def unPark(self, vehicle):
        for floor in self.floors:
            if floor.unPark(vehicle):
                return True
        return False
    
    def display_availability(self):
        for floor in self.floors:
            print(floor.display_availability())
    
    def get_parking_cost(self, vehicle):
        for floor in self.floors:
            cost = floor.get_parking_cost(vehicle)
            if cost:
                return cost
        return 0

    def get_instance(self): 
        return self._instance
    
    