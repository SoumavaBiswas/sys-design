import time
import uuid
import threading
from collections import defaultdict


class Order:
    def __init__(self, customer_id, items, total_price):
        self.order_id = str(uuid.uuid4())  # Unique order ID
        self.customer_id = customer_id
        self.items = items  # List of item IDs
        self.total_price = total_price
        self.order_date = time.time()  # Timestamp of order creation
        self.order_status = "Pending"  # Initial status
        self.payment_status = "Pending"  # Initial payment status

    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.order_status}, Payment: {self.payment_status}"


class Inventory:
    def __init__(self):
        # Holds product_id and its available quantity
        self.products = {
            'p1': {'name': 'Product 1', 'price': 100, 'stock': 50},
            'p2': {'name': 'Product 2', 'price': 200, 'stock': 30},
            'p3': {'name': 'Product 3', 'price': 300, 'stock': 20}
        }
        # Lock to ensure thread-safety when updating stock
        self.lock = threading.Lock()

    def check_stock(self, product_id, quantity):
        with self.lock:  # Acquire lock when checking stock
            return self.products.get(product_id, {}).get('stock', 0) >= quantity

    def update_stock(self, product_id, quantity):
        with self.lock:  # Acquire lock when updating stock
            if product_id in self.products:
                self.products[product_id]['stock'] -= quantity
                print(f"Updated stock for {product_id}: {self.products[product_id]['stock']} units left")


class PaymentService:
    @staticmethod
    def process_payment(order, payment_method):
        # Simulate payment processing logic
        if order.total_price > 0:
            print(f"Processing payment of {order.total_price} using {payment_method}")
            order.payment_status = "Completed"
            return True
        return False


class OrderService:
    def __init__(self, inventory, payment_service):
        self.orders = {}  # store orders in-memory (could be DB)
        self.inventory = inventory
        self.payment_service = payment_service

    def create_order(self, customer_id, items):
        total_price = sum(self.inventory.products[item]['price'] * quantity for item, quantity in items.items())
        
        # Check if inventory is available for the items
        for item, quantity in items.items():
            if not self.inventory.check_stock(item, quantity):
                raise Exception(f"Insufficient stock for {self.inventory.products[item]['name']}")

        order = Order(customer_id, items, total_price)
        self.orders[order.order_id] = order
        return order

    def process_order(self, order_id, payment_method):
        order = self.orders.get(order_id)
        if not order:
            raise Exception(f"Order {order_id} not found.")

        # Check if payment is successful
        payment_success = self.payment_service.process_payment(order, payment_method)
        if payment_success:
            order.order_status = "Processing"
            # Deduct inventory
            for item, quantity in order.items.items():
                self.inventory.update_stock(item, quantity)
            return order
        else:
            raise Exception("Payment failed.")

    def cancel_order(self, order_id):
        order = self.orders.get(order_id)
        if not order:
            raise Exception(f"Order {order_id} not found.")

        if order.order_status == "Processing":
            raise Exception("Cannot cancel an order that is already being processed.")

        order.order_status = "Cancelled"
        return order

    def track_order(self, order_id):
        order = self.orders.get(order_id)
        if not order:
            raise Exception(f"Order {order_id} not found.")
        return str(order)


class NotificationService:
    @staticmethod
    def send_notification(order, status):
        print(f"Sending notification: Order {order.order_id} status updated to {status}")


# Example Usage
inventory = Inventory()
payment_service = PaymentService()
order_service = OrderService(inventory, payment_service)

# Creating an order
items = {'p1': 2, 'p2': 1}  # Example items: 2 Product 1, 1 Product 2
order = order_service.create_order(customer_id="cust123", items=items)
print(order)

# Process payment
order = order_service.process_order(order.order_id, payment_method="Credit Card")
NotificationService.send_notification(order, order.order_status)

# Track order status
print(order_service.track_order(order.order_id))

# Cancel order
order = order_service.cancel_order(order.order_id)
NotificationService.send_notification(order, order.order_status)
