from enum import Enum

class States(Enum):
    IDLE = "IDLE" # No transaction is in progress
    READY = "READY" # Product is selected
    WAITING = "WAITING" # Waiting for amount
    DISPENSE = "DISPENSE" # Dispensing product
    BALANCE = "BALANCE" # Dispensing balance amount
