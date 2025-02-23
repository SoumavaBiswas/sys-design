from VendingMachineDesign.coins import Coins
from VendingMachineDesign.notes import Note


class PaymentProcessor:
    def __init__(self):
        self.balance = 0
    
    def add_coin(self, coin: Coins):
        self.balance += coin.value
    
    def add_note(self, note: Note):
        self.balance += note.value
    
    def make_payment(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def get_change(self):
        return self.balance
    
    def get_balance(self):
        return self.balance