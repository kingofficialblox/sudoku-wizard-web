import time
from generator import SudokuGenerator
import generator


class SudokuLogic:

    def __init__(self, difficulty="MEDIUM"):
        difficulty = difficulty.lower()
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
        self.paused = False
        self.pause_start = 0
        self.notes = [
            [set() for _ in range(9)]
            for _ in range(9)
        ]
        # ---------- Completion Flash ----------
        self.flash_row = None
        self.flash_col = None
        self.flash_box = None

        self.flash_start = 0
        self.flash_duration = 1.4
        self.pop_scale = 1.0
        self.score = 0
        self.stars = 0
        self.accuracy = 100
        self.score_pop_time = 0
        self.score_pop_type = None
        self.score_popup_text = None
        self.score_popup_color = None
        self.score_popup_time = 0
        self.score_popup_y = 0
    
    def get_elapsed_time(self):
        if self.game_won:
            return int(self.end_time - self.start_time)

        if self.paused:
            return int(self.pause_start - self.start_time)

        return int(time.time() - self.start_time)

    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_popup_scale = 0.75
            self.pause_overlay_alpha = 0
            self.pause_buttons_offset = 25
            self.pause_start = time.time()

    def resume(self):
        if self.paused:
            self.start_time += time.time() - self.pause_start
            self.paused = False

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
    def show_score_popup(self, amount):
        if amount > 0:
            self.score_popup_text = f"+{amount}"
            self.score_popup_color = (40, 190, 70)
        else:
            self.score_popup_text = str(amount)
            self.score_popup_color = (220, 50, 50)

        self.score_popup_time = time.time()
        self.score_popup_y = 0

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
            self.score += 100
            self.show_score_popup(100)
            self.score_pop_time = time.time()
            self.score_pop_type = "up"
            self.invalid_cell = None
            self.pop_cell = (row, col)
            self.pop_time = time.time()
            self.pop_scale = 1.6
            self.notes[row][col].clear()
            
            # ---------- Check completed row ----------
            if all(self.grid[row][c] != 0 for c in range(9)):
                self.flash_row = row
                self.score += 500
                self.show_score_popup(500)
                self.score_pop_time = time.time()
                self.score_pop_type = "up"

            # ---------- Check completed column ----------
            if all(self.grid[r][col] != 0 for r in range(9)):
                self.flash_col = col
                self.score += 500
                self.show_score_popup(500)
                self.score_pop_time = time.time()
                self.score_pop_type = "up"

            # ---------- Check completed box ----------
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3

            complete = True

            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if self.grid[r][c] == 0:
                        complete = False

            if complete:
                self.flash_box = (box_row, box_col)
                self.score += 1000
                self.show_score_popup(1000)
                self.score_pop_time = time.time()
                self.score_pop_type = "up"
            # Start flash animation
            if self.flash_row is not None or self.flash_col is not None or self.flash_box is not None:
                self.flash_start = time.time()
            if self.is_solved():
                self.game_won = True
                self.score += 2000
                self.show_score_popup(2000)
                self.score_pop_type = "up"
                self.score_pop_time = time.time()
                self.popup_scale = 0.0
                self.end_time = time.time()

                elapsed = int(self.end_time - self.start_time)

                # ---------- Accuracy ----------
                total_inputs = 81 + self.mistakes

                self.accuracy = round(
                    (81 / total_inputs) * 100
                )               
                # ---------- Stars ----------
                if self.mistakes == 0:
                    self.stars = 5
                elif self.mistakes <= 2:
                    self.stars = 4
                elif self.mistakes <= 4:
                    self.stars = 3
                elif self.mistakes <= 6:
                    self.stars = 2
                else:
                    self.stars = 1

                return "WIN"

            return True
        else:
            self.mistakes += 1
            self.score = max(0, self.score - 150)
            self.show_score_popup(-150)
            self.score_pop_time = time.time()
            self.score_pop_type = "down"
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
        self.score = max(0, self.score - 100)
        self.show_score_popup(-100)
        self.score_pop_time = time.time()
        self.score_pop_type = "down"
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
        self.score = 0
        self.score_pop_time = time.time()
        self.score_pop_type = None
        self.paused = False
        self.pause_start = 0
        self.end_time = None

    def solve(self):
        self.grid = [row[:] for row in self.solution]
        self.score = 0
        self.score_pop_time = time.time()
        self.score_pop_type = "down"
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
    