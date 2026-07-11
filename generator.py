import random


class SudokuGenerator:

    def __init__(self):

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None

    def is_valid(self, row, col, num):

        # Row
        for c in range(9):
            if self.board[row][c] == num:
                return False

        # Column
        for r in range(9):
            if self.board[r][col] == num:
                return False

        # Box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False

        return True
    def fill_board(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.fill_board():
                                return True
                            self.board[row][col] = 0
                    return False
        return True
    def generate(self,difficulty="medium"):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board()
        self.solution = [row[:] for row in self.board]

        self.remove_numbers(difficulty)
        return self.board
    def remove_numbers(self, difficulty="medium"):

        if difficulty == "easy":
            cells_to_remove = 35
        elif difficulty == "hard":
            cells_to_remove = 55
        else:
            cells_to_remove = 45

        removed = 0

        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1