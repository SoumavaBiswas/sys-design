from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from bisect import bisect_left, bisect_right, insort
from collections import defaultdict
import uuid
import threading
from intervaltree import IntervalTree


# -------------------- User Classes --------------------
class User(ABC):
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name


class Customer(User):
    def __init__(self, user_id: str, name: str):
        super().__init__(user_id, name)
        self.bookings = []

    def search_cars(self, rental_service, location, category=None, max_price=None):
        return rental_service.search_cars(location, category, max_price)

    def book_car(self, rental_service, car, pickup_date, return_date, payment_processor):
        booking = rental_service.create_booking(self, car, pickup_date, return_date, payment_processor)
        if booking:
            self.bookings.append(booking)
        return booking

    def cancel_booking(self, booking):
        booking.cancel_booking()
        self.bookings.remove(booking)


class Admin(User):
    def add_car(self, rental_service, car):
        rental_service.add_car(car)

    def remove_car(self, rental_service, car):
        rental_service.remove_car(car)

    def update_price(self, car, new_price):
        car.update_price(new_price)


# -------------------- Car Class --------------------
class Car:
    def __init__(self, car_id, category, price_per_day, location):
        self.car_id = car_id
        self.category = category
        self.price_per_day = price_per_day
        self.location = location
        self.booked_intervals = IntervalTree()
        self.lock = threading.Lock()

    def _to_timestamp(self, date):
        return int(date.timestamp())

    def is_available_for_dates(self, pickup_date, return_date):
        start = self._to_timestamp(pickup_date)
        end = self._to_timestamp(return_date)
        with self.lock:
            return not self.booked_intervals.overlaps(start, end)

    def reserve_car(self, pickup_date, return_date):
        start = self._to_timestamp(pickup_date)
        end = self._to_timestamp(return_date)
        with self.lock:
            if not self.booked_intervals.overlaps(start, end):
                self.booked_intervals[start:end] = True
                return True
            return False

    def return_car(self, pickup_date, return_date):
        start = self._to_timestamp(pickup_date)
        end = self._to_timestamp(return_date)
        with self.lock:
            self.booked_intervals.remove_overlap(start, end)

    def update_price(self, new_price):
        self.price_per_day = new_price


# -------------------- Booking Class --------------------
class Booking:
    def __init__(self, customer, car, pickup_date, return_date):
        self.booking_id = str(uuid.uuid4())
        self.customer = customer
        self.car = car
        self.pickup_date = pickup_date
        self.return_date = return_date
        self.total_price = self.calculate_price()
        self.status = "Confirmed"

    def calculate_price(self):
        return max((self.return_date - self.pickup_date).days, 1) * self.car.price_per_day

    def cancel_booking(self):
        if self.status == "Confirmed":
            self.status = "Cancelled"
            self.car.return_car(self.pickup_date, self.return_date)
            return True
        return False


# -------------------- Payment Processing --------------------
class PaymentProcessor:
    def process_payment(self, amount):
        return f"Payment of ${amount} processed successfully."


# -------------------- Car Rental Service --------------------
class CarRental:
    def __init__(self, name, locations):
        self.name = name
        self.locations = set(locations)
        self.cars_by_location = defaultdict(list)
        self.car_lock = threading.Lock()

    def add_car(self, car):
        with self.car_lock:
            self.cars_by_location[car.location].append(car)

    def remove_car(self, car):
        with self.car_lock:
            self.cars_by_location[car.location].remove(car)

    def search_cars(self, location, category=None, max_price=None, from_date=None, to_date=None):
        if location not in self.locations:
            return []
        
        if from_date and to_date:
            if from_date > to_date:
                raise ValueError("From date must be before to date.")
        
        if not from_date:
            from_date = datetime.now()
        if not to_date:
            to_date = from_date + timedelta(days=1)
        
        cars = self.cars_by_location.get(location, [])
        return [
            car for car in cars
            if car.is_available_for_dates(from_date, to_date) and
            (not category or car.category == category) and
            (not max_price or car.price_per_day <= max_price)
        ]

    def create_booking(self, customer, car, pickup_date, return_date, payment_processor):
        if car.reserve_car(pickup_date, return_date):
            booking = Booking(customer, car, pickup_date, return_date)
            payment_processor.process_payment(booking.total_price)
            return booking
        return None


# -------------------- Example Usage --------------------
if __name__ == "__main__":
    rental_service = CarRental("City Car Rentals", ["Downtown", "Airport"])
    payment_processor = PaymentProcessor()

    car1 = Car("C1", "SUV", 50, "Downtown")
    car2 = Car("C2", "Sedan", 30, "Airport")

    rental_service.add_car(car1)
    rental_service.add_car(car2)

    customer = Customer("C123", "John Doe")

    available_cars = customer.search_cars(rental_service, "Downtown", category="SUV")
    if available_cars:
        booking = customer.book_car(rental_service, available_cars[0], datetime.now(), datetime.now() + timedelta(days=3), payment_processor)
        print(f"Booking ID: {booking.booking_id}, Total Price: ${booking.total_price}, Status: {booking.status}")
        print(f"Car booked: {booking.car.car_id}, Pickup Date: {booking.pickup_date}, Return Date: {booking.return_date}")
    else:
        print("No available cars found.")
    customer.cancel_booking(booking)
    print(f"Booking Status: {booking.status}")
    rental_service.remove_car(car1)
    rental_service.remove_car(car2)
    print("Cars removed successfully.")