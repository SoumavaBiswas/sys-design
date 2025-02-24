import time
from typing import List
from item import Item
from enum import Enum
import uuid

class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"


class Order:
    def __init__(self, uid, food_items:List[Item], aid):
        self.oid = str(uuid.uuid4())
        self.uid = uid
        self.items = food_items
        self.aid = aid
        self.placed_at = time.time()
        self.status = OrderStatus.PLACED
    

    def update_status(self, status):
        self.status = status
    