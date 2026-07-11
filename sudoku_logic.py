import time
from generator import SudokuGenerator
import generator


class SudokuLogic:

    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty.capitalize()

        self.selected = None
        self.highlight_number = None
        self.pop_cell = None
        self.pop_time = 0
        self.shake_cell = None
        self.shake_time = 0
        self.hover = None
        self.end_time = None
        
        

        generator = SudokuGenerator()
        self.grid = generator.generate(difficulty)
        self.solution = generator.solution
        self.original_grid = [row[:] for row in self.grid]

        self.fixed = [[cell != 0 for cell in row]
                      for row in self.grid
        ]
        self.history = []

        
        self.mistakes = 0

        self.invalid_cell = None
        self.invalid_number = None
        self.invalid_time = 0
        self.game_won = False
        self.popup_scale = 0.0
        # Timer
        self.start_time = time.time()
        self.notes = [
            [set() for _ in range(9)]
            for _ in range(9)
        ]

    def select(self, row, col):
        self.selected = (row, col)

        value = self.grid[row][col]

        if value != 0:
            self.highlight_number = value
        else:
            self.highlight_number = None

    def clear_selected(self):

        if self.selected is None:
            return

        row, col = self.selected

        if not self.fixed[row][col]:
            self.grid[row][col] = 0

    def is_valid(self, row, col, number):

        for c in range(9):
            if c != col and self.grid[row][c] == number:
                return False

        for r in range(9):
            if r != row and self.grid[r][col] == number:
                return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col) and self.grid[r][c] == number:
                    return False

        return True

    def place_number(self, number, notes_mode=False):
        if self.selected is None:
            return None

        row, col = self.selected

        if self.fixed[row][col]:
            return None
        # Don't allow editing a correctly filled cell
        if self.grid[row][col] != 0:
            return None

        if notes_mode:
            if number in self.notes[row][col]:
                self.notes[row][col].remove(number)
            else:
                self.notes[row][col].add(number)

            return

        # Save for Undo
        self.history.append((row, col, self.grid[row][col]))

        # Correct number
        if number == self.solution[row][col]:
            self.grid[row][col] = number
            self.invalid_cell = None
            self.pop_cell = (row, col)
            self.pop_time = time.time()
            self.notes[row][col].clear()
            if self.is_solved():
                self.game_won = True
                self.popup_scale = 0.0
                self.end_time = time.time()
                return "WIN"

            return True
        else:
            self.mistakes += 1
            self.invalid_cell = (row, col)
            self.invalid_number = number
            self.invalid_time = time.time()
            return False

    def undo(self):
        if not self.history:
            return
        row, col, value = self.history.pop()
        self.grid[row][col] = value

    def give_hint(self):
        empty_cells = []

        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    empty_cells.append((row, col))

        if not empty_cells:
            return

        import random

        row, col = random.choice(empty_cells)
        self.grid[row][col] = self.solution[row][col]
        self.fixed[row][col] = True

    def restart(self):
        self.grid = [row[:] for row in self.original_grid]
        self.game_won = False

        self.fixed = [
            [cell != 0 for cell in row]
            for row in self.grid
        ]

        self.notes = [
            [set() for _ in range(9)]
            for _ in range(9)
        ]

        self.history.clear()

        self.selected = None

        self.mistakes = 0

        self.invalid_cell = None
        self.invalid_number = None
        self.invalid_time = 0

        self.start_time = time.time()

    def solve(self):
        self.grid = [row[:] for row in self.solution]

        self.fixed = [
            [True for _ in range(9)]
            for _ in range(9)
        ]

    def move_selection(self, dr, dc):
        if self.selected is None:
            self.selected = (0, 0)
            return

        row, col = self.selected
        row = max(0, min(8, row + dr))
        col = max(0, min(8, col + dc))
        self.selected = (row, col)

    def is_conflict(self, row, col):
        value = self.grid[row][col]

        if value == 0:
            return False

        # Check row
        for c in range(9):
            if c != col and self.grid[row][c] == value:
                return True

        # Check column
        for r in range(9):
            if r != row and self.grid[r][col] == value:
                return True

        # Check 3×3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and self.grid[r][c] == value:
                    return True

        return False
    def clear_cell(self):
        if self.selected is None:
            return

        row, col = self.selected

        if self.fixed[row][col]:
            return

        # Save for Undo
        self.history.append(
            (row, col, self.grid[row][col])
        )

        self.grid[row][col] = 0

        self.notes[row][col].clear()
    def is_solved(self):

        for row in range(9):
            for col in range(9):

                value = self.grid[row][col]

                if value == 0:
                    return False

                self.grid[row][col] = 0

                if not self.is_valid(row, col, value):
                    self.grid[row][col] = value
                    return False

                self.grid[row][col] = value

        return True
    def remaining_count(self, number):
        count = 0

        for row in self.grid:
            count += row.count(number)

        return 9 - count
    def count_number(self, number):
        count = 0
        for row in self.grid:
            count += row.count(number)
        return count
