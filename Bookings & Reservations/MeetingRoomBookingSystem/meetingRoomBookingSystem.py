from datetime import datetime
from typing import List
from intervaltree import IntervalTree
import uuid
import threading

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

class Office:
    def __init__(self, office_id: str, location: str):
        self.office_id = office_id
        self.location = location
        self.rooms: dict[str, 'MeetingRoom'] = {}  # room_id -> room

    def add_room(self, room: 'MeetingRoom'):
        self.rooms[room.room_id] = room

class MeetingRoom:
    def __init__(self, room_id: str, name: str, capacity: str, amenties: List):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.amenties = amenties
        self.tree = IntervalTree()
        self.lock = threading.Lock()

    def is_available(self, start: datetime, end: datetime) -> bool:
        # Convert to timestamp for simplicity
        start_ts = start.timestamp()
        end_ts = end.timestamp()
        return len(self.tree.overlap(start_ts, end_ts)) == 0

    def add_booking(self, booking: 'Booking') -> bool:
        start, end = booking.start_time, booking.end_time
        with self.lock:
            if self.is_available(start, end):
                self.tree[start.timestamp():end.timestamp()] = (start, end)
                return True
            return False

    def cancel_booking(self, start: datetime, end: datetime):
        start_ts = start.timestamp()
        end_ts = end.timestamp()
        with self.lock:
            self.tree.remove_overlap(start_ts, end_ts)

class Booking:
    def __init__(self, booking_id: str, user: User, room: MeetingRoom, start_time: datetime, end_time: datetime):
        self.booking_id = booking_id
        self.user = user
        self.room = room
        self.start_time = start_time
        self.end_time = end_time


class BookingService:
    def __init__(self):
        self.offices: dict[str, Office] = {}

    def add_office(self, office: Office):
        self.offices[office.office_id] = office

    def book_room(self, user: User, office_id: str, room_id: str, start: datetime, end: datetime) -> str:
        office = self.offices.get(office_id)
        if not office:
            return "Office not found"
        room = office.rooms.get(room_id)
        if not room:
            return "Room not found"
        booking = Booking(str(uuid.uuid4()), user, room, start, end)
        if room.add_booking(booking):
            return f"Booking confirmed: {booking.booking_id}"
        return "Room not available for selected time slot"

    def search_available_rooms(self, office_id: str, start: datetime, end: datetime, min_capacity: int = 1) -> List[MeetingRoom]:
        office = self.offices.get(office_id)
        if not office:
            return []
        return [room_id for room_id, room in office.rooms.items() if room.capacity >= min_capacity and room.is_available(start, end)]


# Setup
office = Office("O1", "Kolkata HQ")
room1 = MeetingRoom("R1", "Conf Room A", 10, ["Projector"])
room2 = MeetingRoom("R2", "Conf Room B", 5, ["Whiteboard"])
office.add_room(room1)
office.add_room(room2)

service = BookingService()
service.add_office(office)

# Book
from datetime import datetime, timedelta

user = User("U1", "Soumava")
start = datetime(2025, 5, 14, 10, 0)
end = datetime(2025, 5, 14, 11, 0)

print(service.book_room(user, "O1", "R1", start, end))
print(service.search_available_rooms("O1", start, end, min_capacity=5))
