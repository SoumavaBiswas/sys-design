from ParkingLotDesign.parkingFloor import ParkingFloor
from ParkingLotDesign.vehicle import Bike, Car, Truck, VehicleType
from ParkingLotDesign.parkingLot import ParkingLot
from ParkingLotDesign.parkingSpot import ParkingSpot


class ParkingLotDemo:
    @staticmethod
    def run():
        parkingLot = ParkingLot()
        parkingLot.add_parking_floor(ParkingFloor(1, 10, VehicleType.TRUCK))
        parkingLot.add_parking_floor(ParkingFloor(2, 10, VehicleType.CAR))
        parkingLot.add_parking_floor(ParkingFloor(3, 10, VehicleType.BIKE))   
        bike = Bike("MH-02-1234")
        car = Car("MH-02-1235")
        truck = Truck("MH-02-1236")
        parkingLot.park(bike)
        parkingLot.park(car)
        parkingLot.park(truck)
        parkingLot.display_availability()
        parkingLot.unPark(bike)
        parkingLot.display_availability()
        parkingLot.unPark(car)
        parkingLot.display_availability()
        parkingLot.unPark(truck)
        parkingLot.display_availability()


if __name__ == "__main__":
    ParkingLotDemo.run()