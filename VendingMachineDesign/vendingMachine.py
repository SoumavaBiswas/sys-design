from VendingMachineDesign.inventory import Inventory
from VendingMachineDesign.paymentProcessor import PaymentProcessor
from VendingMachineDesign.stateManager import StateManager
from VendingMachineDesign.states import States
from VendingMachineDesign.coins import Coins
from VendingMachineDesign.notes import Note
from threading import Lock


class VendingMachine:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(VendingMachine, cls).__new__(cls)
                cls._instance.inventory = Inventory()
                cls._instance.paymentProcessor = PaymentProcessor()
                cls._instance.stateManager = StateManager()
        return cls._instance
    
        

    def add_product(self, product, quantity):
        return self.inventory.add_product(product, quantity)
    
    def select_product(self, product):
        if self.stateManager.select_product():
            return self.inventory.select_product(product)
    
    def dispense_product(self):
        if self.stateManager.dispense_product():
            product = self.inventory.get_selected_product()
            if self.paymentProcessor.make_payment(product.price):
                return self.inventory.dispense_product()
        return "Sorry! Could not dispense the product. Please try again."
        
        
    def add_coin(self, coin: Coins):
        if self.stateManager.add_coin():
            self.paymentProcessor.add_coin(coin)
            product_price = self.inventory.get_selected_product().price
            current_balance = self.paymentProcessor.get_balance()
            if current_balance >= product_price:
                self.stateManager.set_state(States.DISPENSE)
                return f"Amount ({coin.value}) added. Balance is sufficient. Please collect the dispensed product."
            return f"Amount ({coin.value}) added. Please add {product_price - current_balance} more."
        
    def add_note(self, note: Note):
         if self.stateManager.add_note():
            self.paymentProcessor.add_note(note)
            product_price = self.inventory.get_selected_product().price
            current_balance = self.paymentProcessor.get_balance()
            if current_balance >= product_price:
                self.stateManager.set_state(States.DISPENSE)
                return f"Amount ({note.value}) added. Balance is sufficient. Please collect the dispensed product."
            return f"Amount ({note.value}) added. Please add {product_price - current_balance} more."

    def get_change(self):
        if self.stateManager.get_change():
            return f'Balance ({self.paymentProcessor.get_change()}) returned successfully.'
        return "No change available"

    