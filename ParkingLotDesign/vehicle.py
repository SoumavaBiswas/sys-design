from abc import ABC
from enum import Enum

class VehicleType(Enum):
    CAR = "car"
    BIKE = "bike"
    TRUCK = "truck"


class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: str):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

    def __str__(self):
        return f"{self.vehicle_type} with license plate {self.license_plate}"

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)
        


class Bike(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BIKE)
    

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)
        