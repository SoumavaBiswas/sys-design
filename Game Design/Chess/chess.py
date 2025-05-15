from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

class Player:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color

class Cell:
    def __init__(self, x: int, y: int, piece: Optional['Piece'] = None):
        self.x = x
        self.y = y
        self.piece = piece

class Board:
    def __init__(self):
        self.cells = [[Cell(i, j) for j in range(8)] for i in range(8)]
        self.setup_board()

    def setup_board(self):
        # Setup pawns
        for i in range(8):
            self.cells[1][i].piece = Pawn(Color.BLACK)
            self.cells[6][i].piece = Pawn(Color.WHITE)

        # Setup major pieces
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece_cls in enumerate(pieces):
            self.cells[0][i].piece = piece_cls(Color.BLACK)
            self.cells[7][i].piece = piece_cls(Color.WHITE)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[x][y]

class Piece(ABC):
    def __init__(self, color: Color):
        self.color = color

    @abstractmethod
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        pass

class King(Piece):
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)
        return max(dx, dy) == 1

class Queen(Piece):
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)
        return dx == dy or start.x == end.x or start.y == end.y

class Rook(Piece):
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        return start.x == end.x or start.y == end.y

class Bishop(Piece):
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        return abs(start.x - end.x) == abs(start.y - end.y)

class Knight(Piece):
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        dx = abs(start.x - end.x)
        dy = abs(start.y - end.y)
        return (dx, dy) in [(1, 2), (2, 1)]

class Pawn(Piece):
    def is_valid_move(self, board: Board, start: Cell, end: Cell) -> bool:
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1

        dx = end.x - start.x
        dy = abs(end.y - start.y)

        if dy == 0 and dx == direction and end.piece is None:
            return True
        if dy == 0 and dx == 2 * direction and start.x == start_row and end.piece is None:
            return True
        if dy == 1 and dx == direction and end.piece is not None and end.piece.color != self.color:
            return True
        return False

class Move:
    def __init__(self, start: Cell, end: Cell, piece: Piece, captured: Optional[Piece]):
        self.start = start
        self.end = end
        self.piece = piece
        self.captured = captured

class ChessGame:
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.players = [player1, player2]
        self.current_turn = 0
        self.moves: List[Move] = []

    def make_move(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        start = self.board.get_cell(start_x, start_y)
        end = self.board.get_cell(end_x, end_y)
        piece = start.piece

        if not piece or piece.color != self.players[self.current_turn].color:
            return False

        if piece.is_valid_move(self.board, start, end):
            captured = end.piece
            end.piece = piece
            start.piece = None
            self.moves.append(Move(start, end, piece, captured))
            self.current_turn = 1 - self.current_turn
            return True

        return False

    def print_board(self):
        for row in self.board.cells:
            print(" ".join([type(cell.piece).__name__[0] if cell.piece else '.' for cell in row]))
