from datetime import datetime
from enum import Enum
from uuid import uuid4
from threading import Lock
from intervaltree import Interval, IntervalTree

# Enums
class RoomType(Enum):
    SINGLE = 'single'
    DOUBLE = 'double'
    SUITE = 'suite'

class BookingStatus(Enum):
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'

# Exceptions
class BookingError(Exception): pass
class PaymentError(Exception): pass

# Models
class Room:
    def __init__(self, room_id: str, room_type: RoomType, price: float):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.bookings = IntervalTree()
        self.lock = Lock()

    def is_available(self, start_date: datetime, end_date: datetime) -> bool:
        return not self.bookings.overlaps(start_date.timestamp(), end_date.timestamp())

    def book(self, start_date: datetime, end_date: datetime):
        self.bookings.add(Interval(start_date.timestamp(), end_date.timestamp()))

    def cancel(self, start_date: datetime, end_date: datetime):
        self.bookings.remove_overlap(start_date.timestamp(), end_date.timestamp())

class Customer:
    def __init__(self, name: str):
        self.customer_id = str(uuid4())
        self.name = name

class Booking:
    def __init__(self, customer: Customer, room: Room, start_date: datetime, end_date: datetime):
        self.booking_id = str(uuid4())
        self.customer = customer
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.status = BookingStatus.CONFIRMED
        self.total_price = self.calculate_price()

    def calculate_price(self) -> float:
        nights = (self.end_date - self.start_date).days
        return nights * self.room.price

    def cancel(self):
        self.status = BookingStatus.CANCELLED
        self.room.cancel(self.start_date, self.end_date)

class PaymentProcessor:
    @staticmethod
    def process_payment(customer: Customer, amount: float) -> bool:
        return True  # Assume payment is always successful

# Admin System
class HotelBookingSystem:
    def __init__(self):
        self.rooms = {}
        self.bookings = {}
        self.customers = {}

    def add_room(self, room_id: str, room_type: RoomType, price: float):
        self.rooms[room_id] = Room(room_id, room_type, price)

    def register_customer(self, name: str) -> Customer:
        customer = Customer(name)
        self.customers[customer.customer_id] = customer
        return customer

    def find_available_room(self, room_type: RoomType, start_date: datetime, end_date: datetime):
        for room in self.rooms.values():
            if room.room_type == room_type and room.is_available(start_date, end_date):
                return room
        return None

    def book_room(self, customer_id: str, room_type: RoomType, start_date: datetime, end_date: datetime) -> Booking:
        customer = self.customers.get(customer_id)
        if not customer:
            raise BookingError("Invalid customer")

        room = self.find_available_room(room_type, start_date, end_date)
        if not room:
            raise BookingError("No rooms available")

        with room.lock:
            if not room.is_available(start_date, end_date):
                raise BookingError("Room became unavailable")

            booking = Booking(customer, room, start_date, end_date)
            if not PaymentProcessor.process_payment(customer, booking.total_price):
                raise PaymentError("Payment failed")

            room.book(start_date, end_date)
            self.bookings[booking.booking_id] = booking
            return booking

    def cancel_booking(self, booking_id: str):
        booking = self.bookings.get(booking_id)
        if not booking or booking.status == BookingStatus.CANCELLED:
            raise BookingError("Invalid or already cancelled booking")
        booking.cancel()
