from VendingMachineDesign.states import States


class StateManager():
    def __init__(self):
        self.state = States.IDLE
    
    def set_state(self, state):
        self.state = state
    
    def select_product(self):
        if self.state == States.IDLE:
            self.state = States.READY
            return True
        elif self.state == States.READY:
            print("Product already selected")
            return False
        elif self.state == States.WAITING:
            print("Product is already selected. Please make the payment.")
            return False
        elif self.state == States.DISPENSE:
            print("Please collect the dispensed product first.")
            return False
        elif self.state == States.BALANCE:
            print("Please collect the balance for previous transaction.")
            return False
    
    def add_money(self):
        if self.state == States.IDLE:
            print("Please select a product first.")
            return False
        elif self.state == States.READY:
            self.state = States.WAITING
            return True
        elif self.state == States.WAITING:
            self.state = States.WAITING
            return True
        elif self.state == States.DISPENSE:
            print("Please collect the dispensed product first.")
            return False
        elif self.state == States.BALANCE:
            print("Please collect the balance for previous transaction.")
            return False
    
    
    def dispense_product(self):
        if self.state == States.IDLE:
            print("Please select a product first.")
            return False
        elif self.state == States.READY:
            print("Please add the amount first.")
            return False
        elif self.state == States.WAITING:
            print("Insufficient amount. Please add more.")
            return False
        elif self.state == States.DISPENSE:
            self.state = States.BALANCE
            return True
        elif self.state == States.BALANCE:
            print("Product is already dispensed. Please collect the balance.")
            return False
    
    def get_change(self):
        if self.state == States.BALANCE:
            self.state = States.IDLE
            return True
        elif self.state == States.DISPENSE:
            print("Please collect the dispensed product first.")
            return False
        else:
            print("No balance to dispense.")
            return False
    
    



