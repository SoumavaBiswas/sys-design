import uuid

class Item:
    def __init__(self, name, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
    

    def __str__(self):
        return f"Item(name={self.name}, price={self.price})"
    
