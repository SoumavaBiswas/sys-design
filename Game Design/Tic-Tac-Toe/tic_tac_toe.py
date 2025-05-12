class Board:
    def __init__(self, n):
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag1 = 0
        self.diag2 = 0
        self.winner = 0
        self.size = n
    

    def move(self, row, col, player):
        self.rows[row] += player
        self.cols[col] += player
        if row == col:
            self.diag1 += player
        if row + col == self.size - 1:
            self.diag2 += player
        if (abs(self.rows[row]) == self.size or
            abs(self.cols[col]) == self.size or
            abs(self.diag1) == self.size or
            abs(self.diag2) == self.size):
            self.winner = player
            return True
        return False

    def getWinner(self):
        return self.winner


class TicTacToe:
    def __init__(self, n):
        self.board = Board(n)
        self.size = n
        self.player1 = 1
        self.player2 = -1

    def move(self, row, col, player):
        if player == 1:
            player = self.player1
        else:
            player = self.player2
        if self.board.move(row, col, player):
            return True
        return False

    def getWinner(self):
        return self.board.getWinner()


# Example usage
if __name__ == "__main__":
    n = 3
    game = TicTacToe(n)
    print(game.move(0, 0, 1))  # Player 1 moves
    print(game.move(0, 1, 2))  # Player 2 moves
    print(game.move(1, 1, 1))  # Player 1 moves
    print(game.move(0, 2, 2))  # Player 2 moves
    print(game.move(2, 2, 1))  # Player 1 moves
    print(game.getWinner())    # Check winner