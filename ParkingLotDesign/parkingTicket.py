import time
from vehicle import VehicleType
from ParkingLotDesign.parkingCostChart import ParkingCostChart

class ParkingTicket:
    def __init__(self, ticket_id, vehicle_type: VehicleType):
        self.ticket_id = ticket_id
        self.vehicle_type = vehicle_type
        self.entry_time = time.time()

    
    def get_cost(self):
        cost_per_hour = ParkingCostChart[self.vehicle_type]
        total_time = time.time() - self.entry_time
        total_hours = total_time / 3600
        return total_hours * cost_per_hour