from order import Order, OrderStatus

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
