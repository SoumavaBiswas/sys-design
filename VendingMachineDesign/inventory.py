from VendingMachineDesign.products import Product


class Inventory:
    def __init__(self):
        self.items = {}
        self.selected_product = None
    
    def select_product(self, product: Product) -> str:
        if not self.check_availability(product):
            return f"{product.name} is out of stock"
        self.selected_product = product
        return f"{product.name} selected. Please make the payment."
    
    def get_selected_product(self) -> Product:
        return self.selected_product
        
        
    def add_product(self, product: Product, quantity: int) -> str:
        if product in self.items:
            self.items[product.name] += quantity
            return f"{quantity} {product.name} added to inventory"
        else:
            self.items[product.name] = quantity
            return f"{quantity} {product.name} added to inventory"
    
    def check_availability(self, product: Product) -> bool:
        return product.name in self.items and self.items[product.name] > 0
    
    def dispense_product(self) -> str:
            product = self.selected_product
            self.items[product.name] -= 1
            return f"{product.name} dispensed successfully."
    