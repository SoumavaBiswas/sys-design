from VendingMachineDesign.products import Coke, Pepsi, Lays, Snickers
from VendingMachineDesign.vendingMachine import VendingMachine
from VendingMachineDesign.coins import Coins
from VendingMachineDesign.notes import Note

class VendingMachineDemo:
    def run(self):

        coke = Coke()
        pepsi = Pepsi()
        lays = Lays()
        snickers = Snickers()

        vendingMachine = VendingMachine()
        
        print(vendingMachine.add_product(coke, 10))
        print(vendingMachine.add_product(pepsi, 10))
        print(vendingMachine.add_product(lays, 10))
        print(vendingMachine.add_product(snickers, 10))

        print(vendingMachine.select_product(coke))
        print(vendingMachine.add_coin(Coins.TEN))
        print(vendingMachine.dispense_product())
        print(vendingMachine.add_note(Note.TWENTY))
        print(vendingMachine.get_change())
        print(vendingMachine.dispense_product())
        print(vendingMachine.get_change())


if __name__ == "__main__":
    vendingMachineDemo = VendingMachineDemo()
    vendingMachineDemo.run()

        