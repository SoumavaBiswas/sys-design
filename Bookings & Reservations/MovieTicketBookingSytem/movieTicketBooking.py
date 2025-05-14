from datetime import datetime
from enum import Enum
from threading import Lock
from uuid import uuid4

class SeatType(Enum):
    REGULAR = "regular"
    PREMIUM = "premium"
    VIP = "vip"

class Seat:
    def __init__(self, seat_id: str, row: str, number: int, seat_type: SeatType):
        self.seat_id = seat_id
        self.row = row
        self.number = number
        self.seat_type = seat_type

class Screen:
    def __init__(self, screen_id: str, seats: list[Seat]):
        self.screen_id = screen_id
        self.seats = {seat.seat_id: seat for seat in seats}

class Show:
    def __init__(self, show_id: str, movie_name: str, venue_id: str, screen: Screen, start_time: datetime, end_time: datetime):
        self.show_id = show_id
        self.movie_name = movie_name
        self.venue_id = venue_id
        self.screen = screen
        self.start_time = start_time
        self.end_time = end_time
        self.lock = Lock()
        self.booked_seats = set()

    def is_seat_available(self, seat_id: str) -> bool:
        return seat_id not in self.booked_seats

    def book_seats(self, seat_ids: list[str]) -> bool:
        with self.lock:
            if any(seat_id in self.booked_seats for seat_id in seat_ids):
                return False
            self.booked_seats.update(seat_ids)
            return True

    def cancel_seats(self, seat_ids: list[str]):
        with self.lock:
            for seat_id in seat_ids:
                self.booked_seats.discard(seat_id)

class Venue:
    def __init__(self, venue_id: str, name: str, city: str, screens: list[Screen]):
        self.venue_id = venue_id
        self.name = name
        self.city = city
        self.screens = {screen.screen_id: screen for screen in screens}

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

class BookingStatus(Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class Booking:
    def __init__(self, user: User, show: Show, seat_ids: list[str]):
        self.booking_id = str(uuid4())
        self.user = user
        self.show = show
        self.seat_ids = seat_ids
        self.status = BookingStatus.CONFIRMED
        self.total_amount = self.calculate_price()

    def calculate_price(self):
        return 200 * len(self.seat_ids)  # Simplified flat rate

    def cancel(self):
        if self.status == BookingStatus.CONFIRMED:
            self.show.cancel_seats(self.seat_ids)
            self.status = BookingStatus.CANCELLED

class PaymentService:
    @staticmethod
    def process_payment(user: User, amount: float) -> bool:
        return True  # Assume payment success

class BookMyShowService:
    def __init__(self):
        self.users = {}
        self.venues = {}
        self.shows = {}
        self.bookings = {}

    def register_user(self, name: str) -> User:
        user = User(str(uuid4()), name)
        self.users[user.user_id] = user
        return user

    def add_venue(self, venue: Venue):
        self.venues[venue.venue_id] = venue

    def add_show(self, show: Show):
        self.shows[show.show_id] = show

    def search_shows(self, city: str, movie_name: str) -> list[Show]:
        city_venue_ids = {v.venue_id for v in self.venues.values() if v.city == city}
        return [show for show in self.shows.values()
                if show.movie_name == movie_name and show.venue_id in city_venue_ids]

    def book_tickets(self, user_id: str, show_id: str, seat_ids: list[str]) -> Booking:
        user = self.users[user_id]
        show = self.shows[show_id]
        if not show.book_seats(seat_ids):
            raise Exception("Some seats are already booked")

        booking = Booking(user, show, seat_ids)
        if not PaymentService.process_payment(user, booking.total_amount):
            show.cancel_seats(seat_ids)
            raise Exception("Payment Failed")

        self.bookings[booking.booking_id] = booking
        return booking

    def cancel_booking(self, booking_id: str):
        booking = self.bookings.get(booking_id)
        if booking:
            booking.cancel()


if __name__ == "__main__":
    service = BookMyShowService()
    user = service.register_user("Soumava")

    seats = [Seat(f"S{i}", "A", i, SeatType.REGULAR) for i in range(1, 11)]
    screen = Screen("SCR1", seats)
    venue = Venue("VEN1", "Inox City Mall", "Kolkata", [screen])
    service.add_venue(venue)

    show = Show("SH1", "Avengers", venue.venue_id, screen, datetime(2025, 5, 20, 18), datetime(2025, 5, 20, 21))
    service.add_show(show)

    booking = service.book_tickets(user.user_id, "SH1", ["S1", "S2"])
    print(f"Booking ID: {booking.booking_id}, Amount: {booking.total_amount}")
    service.cancel_booking(booking.booking_id)
