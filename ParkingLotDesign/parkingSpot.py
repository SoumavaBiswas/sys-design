from ParkingLotDesign.vehicle import Vehicle

class ParkingSpot:
    def __init__(self, spot_number: int, vehicle_type: str):
        self.spot_number = spot_number
        self.vehicle_type = vehicle_type
        self.vehicle = None
        self.is_available = True
    
    def park(self, vehicle: Vehicle):
        if self.is_available and self.vehicle_type == vehicle.vehicle_type:
            self.vehicle = vehicle
            self.is_available = False
            return True
        return False
    
    def unPark(self, vehicle: Vehicle):
        if not self.is_available and self.vehicle == vehicle:
            self.vehicle = None
            self.is_available = True
            return True
        return False
    
    def isAvailable(self):
        return self.is_available