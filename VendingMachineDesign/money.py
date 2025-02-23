from abc import ABC
from enum import Enum

class CoinType(Enum):
    ONE = 1
    TWO = 2
    FIVE = 5
    TEN = 10
    TWENTY = 20

class NoteType(Enum):
    HUNDRED = 100
    FIFTY = 50
    TWENTY = 20
    TEN = 10

class Money(ABC):
    def __init__(self, value: int):
        self.value = value


class Coin(Money):
    def __init__(self, coin_type: CoinType):
        super().__init__(coin_type.value)

class Note(Money):
    def __init__(self, note_type: NoteType):
        super().__init__(note_type.value)