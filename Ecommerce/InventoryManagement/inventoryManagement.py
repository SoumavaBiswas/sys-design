import threading


class Product:
    def __init__(self, product_id, name, initial_stock=0, threshold=5):
        self.product_id = product_id
        self.name = name
        self.stock = initial_stock
        self.threshold = threshold
        self.lock = threading.Lock()

    def add_stock(self, quantity):
        with self.lock:
            self.stock += quantity
            print(f"Added {quantity} units to {self.name}. Current stock: {self.stock}")

    def reduce_stock(self, quantity):
        with self.lock:
            if self.stock >= quantity:
                self.stock -= quantity
                print(f"Reduced {quantity} units from {self.name}. Current stock: {self.stock}")
                if self.stock < self.threshold:
                    print(f"⚠️ Warning: Stock for {self.name} is below threshold.")
                return True
            else:
                print(f"❌ Not enough stock for {self.name}. Available: {self.stock}, Requested: {quantity}")
                return False

    def get_stock(self):
        with self.lock:
            return self.stock


class Inventory:
    def __init__(self):
        self.products = {}
        self.inventory_lock = threading.Lock()

    def add_product(self, product_id, name, initial_stock=0, threshold=5):
        with self.inventory_lock:
            if product_id in self.products:
                raise Exception(f"Product {product_id} already exists.")
            self.products[product_id] = Product(product_id, name, initial_stock, threshold)
            print(f"✅ Product '{name}' added to inventory.")

    def add_stock(self, product_id, quantity):
        if product_id not in self.products:
            raise Exception("Product not found")
        self.products[product_id].add_stock(quantity)

    def reduce_stock(self, product_id, quantity):
        if product_id not in self.products:
            raise Exception("Product not found")
        return self.products[product_id].reduce_stock(quantity)

    def get_stock(self, product_id):
        if product_id not in self.products:
            raise Exception("Product not found")
        return self.products[product_id].get_stock()

    def get_all_inventory(self):
        return {
            pid: {
                "name": product.name,
                "stock": product.get_stock()
            } for pid, product in self.products.items()
        }



if __name__ == "__main__":
    inventory = Inventory()
    inventory.add_product("P001", "iPhone 15", 10, threshold=3)
    inventory.add_product("P002", "Macbook Pro", 5)

    inventory.add_stock("P001", 5)
    inventory.reduce_stock("P001", 12)  # Should trigger low stock warning
    print(inventory.get_all_inventory())
