from VendingMachineDesign.money import Money
class PaymentProcessor:
    def __init__(self):
        self.balance = 0
    
    def add_money(self, money: Money):
        self.balance += money.value
    
    def make_payment(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f'Payment successful. Balance: {self.balance}')
            return True
        return False
    
    def get_change(self):
        return self.balance
    
    def get_balance(self):
        return self.balance