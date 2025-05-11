from abc import ABC, abstractmethod
import uuid
from enum import Enum
from intervaltree import IntervalTree
import threading
from datetime import datetime, timedelta
from collections import defaultdict


class RoomType(Enum):
    STANDRAD = "Standard"
    DELUXE = "Deluxe"
    PREMIUM = "Premium"


class BookingStatus:
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

class Room:
    def __init__(self, room_no):
        self.id = str(uuid.uuid4())[:6]
        self.room_no = room_no
        self.booked_interval = IntervalTree()
        self.lock = threading.Lock()
    
    def _to_timestamp(self, date:datetime):
        return int(date.timestamp())

    def is_available_for_dates(self, from_date, to_date):
        start = self._to_timestamp(from_date)
        end = self._to_timestamp(to_date)
        if self.booked_interval.overlaps(start, end):
            return False
        return True
    

    def reserve_booking(self, from_date, to_date):
        start = self._to_timestamp(from_date)
        end = self._to_timestamp(to_date)
       
        with self.lock:
             if not self.booked_interval.overlaps(start, end):
                self.booked_interval[start: end] = True
                return True
             return False
    
    def cancel_booking(self, from_date, to_date):
        start = self._to_timestamp(from_date)
        end = self._to_timestamp(to_date)
       
        with self.lock:
            self.booked_interval.remove_overlap(start, end)

            


class StandardRoom(Room):
    def __init__(self, room_no):
        super().__init__(room_no)
        self.room_type = RoomType.STANDRAD
        self.price_per_night = 100

class DeluxeRoom(Room):
    def __init__(self, room_no):
        super().__init__(room_no)
        self.room_type = RoomType.DELUXE
        self.price_per_night = 150

class PremiumRoom(Room):
    def __init__(self, room_no):
        super().__init__(room_no)
        self.room_type = RoomType.PREMIUM
        self.price_per_night = 200


class RentalSystem:
    def __init__(self):
        self.rooms = defaultdict(list)  # RoomType -> List[Room]
        self.customers = []
        self.room_lock = threading.Lock()
    
    def add_room(self, room: Room):
        self.rooms[room.room_type].append(room)
    
    def remove_room(self, room: Room):
        if room.room_type in self.rooms:
            self.rooms[room.room_type].remove(room)

    def search_room(self, from_date=None, to_date=None, room_type=None):
        if not from_date:
            from_date = datetime.now()
        if not to_date:
            to_date = from_date + timedelta(days=1)

        result = []

        if room_type:
            rooms_to_search = self.rooms.get(room_type, [])
        else:
            # Flatten all room lists
            rooms_to_search = [room for room_list in self.rooms.values() for room in room_list]

        for room in rooms_to_search:
            if room.is_available_for_dates(from_date, to_date):
                result.append(room)
        
        return result

    def create_booking(self, customer, room, from_date, to_date, payment_processor):
        with self.room_lock:
            if room.is_available_for_dates(from_date, to_date):
                booking = Booking(customer, room, from_date, to_date, payment_processor)
                room.reserve_booking(from_date, to_date)
                payment_processor.process_payment(booking.price)
                return booking
        return None


class PaymentProcessor:
    def process_payment(self, amount):
        return f"Payment of ${amount} processed successfully."
    
    def refund(self, amount):
        return f"Refund initiated of ${amount}."




class Booking:
    def __init__(self, customer, room:Room, from_date:datetime, to_date:datetime, payment_processor: PaymentProcessor):
        self.id = str(uuid.uuid4())[:6]
        self.customer = customer
        self.room = room
        self.from_date = from_date
        self.to_date = to_date
        self.price = self.calculate_price()
        self.status = BookingStatus.CONFIRMED
        self.payment_processor = payment_processor
    
    def calculate_price(self):
        return (self.to_date-self.from_date).days * self.room.price_per_night

    def cancel_booking(self):
        if self.status == BookingStatus.CONFIRMED:
            self.status = BookingStatus.CANCELLED
            self.room.cancel_booking(self.from_date, self.to_date)
            self.payment_processor.refund(self.price)
            return True
        return False


class User(ABC):
    def __init__(self, username):
        self.id = str(uuid.uuid4())[:6]
        self.username = username



class Customer(User):
    def __init__(self, username):
        super().__init__(username)
        self.bookings = []
    

    def create_booking(self, rental_system: RentalSystem, room: Room, from_date: datetime, to_date: datetime, payment_processor: PaymentProcessor):
        booking = rental_system.create_booking(self, room, from_date, to_date, payment_processor)
        if booking:
            self.bookings.append(booking)

    def cancel_booking(self, booking: Booking):
        if booking.cancel_booking():
            self.bookings.remove(booking)

    def search_rooms(self, rental_system: RentalSystem, from_date:datetime, to_date:datetime, room_type=None):
        return rental_system.search_room(from_date, to_date, room_type)

class Admin(User):
    def __init__(self, username):
        super().__init__(username)
    
    def add_room(self, rental_system: RentalSystem, room: Room):
        rental_system.add_room(room)

    def remove_room(self, rental_system: RentalSystem, room: Room):
        rental_system.remove_room(room)




if __name__ == "__main__":
    # Setup system
    rental_system = RentalSystem()
    admin = Admin("admin123")

    # Add rooms
    room1 = StandardRoom("101")
    room2 = DeluxeRoom("201")
    room3 = PremiumRoom("301")

    admin.add_room(rental_system, room1)
    admin.add_room(rental_system, room2)
    admin.add_room(rental_system, room3)

    # Setup customer and payment processor
    customer = Customer("soumava")
    payment_processor = PaymentProcessor()

    # Define booking dates
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)

    # Search available Deluxe rooms
    available_rooms = customer.search_rooms(rental_system, today, tomorrow)
    print("Available Rooms:")
    for r in available_rooms:
        print(f" - Room No: {r.room_no}, ID: {r.id}")

    # Book the first available deluxe room
    if available_rooms:
        customer.create_booking(rental_system, available_rooms[0], today, tomorrow, payment_processor)
        print("\nBooking created!")

    # Try searching again - should show no deluxe rooms
    print("\nAfter booking:")
    available_rooms = customer.search_rooms(rental_system, today, tomorrow)
    print("Available Rooms:")
    for r in available_rooms:
        print(f" - Room No: {r.room_no}, ID: {r.id}")
    
    # Cancel the booking
    if customer.bookings:
        booking = customer.bookings[0]
        customer.cancel_booking(booking)
        print("\nBooking cancelled!")

    # Final check
    print("\nAfter cancellation:")
    available_rooms = customer.search_rooms(rental_system, today, tomorrow, RoomType.DELUXE)
    print("Available Deluxe Rooms:")
    for r in available_rooms:
        print(f" - Room No: {r.room_no}, ID: {r.id}")









