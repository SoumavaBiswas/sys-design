import time
from typing import List
from enum import Enum
import uuid

class Item:
    def __init__(self, name, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
    

    def __str__(self):
        return f"Item(name={self.name}, price={self.price})"
    


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
    


class OrderService:
    def __init__(self):
        self.orders = {}
    

    def palce_order(self, order: Order):
        self.orders[order.oid] = order
    
    def update_status(self, oid, status: OrderStatus):
        order = self.orders.get(oid)
        if order:
            order.update_status(status)
    
    def get_order(self, oid):
        return self.orders.get(oid)
