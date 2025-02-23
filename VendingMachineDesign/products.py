from abc import ABC

class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Coke(Product):
    def __init__(self):
        super().__init__("Coke", 25)

class Pepsi(Product):
    def __init__(self):
        super().__init__("Pepsi", 35)

class Lays(Product):
    def __init__(self):
        super().__init__("Lays", 15)

class Snickers(Product):
    def __init__(self):
        super().__init__("Snickers", 20)

