"""
Sudoku puzzle generator using backtracking algorithm.
"""

import random
from typing import List


class SudokuGenerator:
    """Generate random valid Sudoku puzzles with specified difficulty levels."""

    # Difficulty settings: number of cells to remove
    DIFFICULTY_LEVELS = {
        "EASY": 35,
        "MEDIUM": 45,
        "HARD": 55,
    }

    def __init__(self) -> None:
        """Initialize generator with empty board."""
        self.board: List[List[int]] = [[0 for _ in range(9)] for _ in range(9)]
        self.solution: List[List[int]] = []

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Check if placing num at (row, col) is valid.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            num: Number to place (1-9)
            
        Returns:
            True if placement is valid, False otherwise
        """
        # Check row
        for c in range(9):
            if self.board[row][c] == num:
                return False

        # Check column
        for r in range(9):
            if self.board[r][col] == num:
                return False

        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False

        return True

    def fill_board(self) -> bool:
        """
        Fill the board using backtracking algorithm.
        
        Returns:
            True if board is successfully filled, False otherwise
        """
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
                            
                            # Backtrack
                            self.board[row][col] = 0
                    
                    return False
        
        return True

    def generate(self, difficulty: str = "MEDIUM") -> List[List[int]]:
        """
        Generate a complete Sudoku puzzle.
        
        Args:
            difficulty: "EASY", "MEDIUM", or "HARD"
            
        Returns:
            The puzzle board with some cells removed
        """
        # A puzzle is accepted only when it has one solution and can be
        # completed through standard logical singles—never a forced guess.
        for _ in range(40):
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self.fill_board()
            self.solution = [row[:] for row in self.board]
            if self.remove_numbers(difficulty):
                return self.board
        # The fallback still preserves uniqueness and logical solvability;
        # it may simply contain a few more clues on a very unlucky seed.
        return self.board

    @staticmethod
    def _candidates(grid: List[List[int]], row: int, col: int) -> set[int]:
        if grid[row][col]:
            return set()
        used = set(grid[row])
        used.update(grid[r][col] for r in range(9))
        box_row, box_col = row // 3 * 3, col // 3 * 3
        used.update(grid[r][c] for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3))
        return set(range(1, 10)) - used

    @classmethod
    def _next_logical_move(cls, grid: List[List[int]]):
        """Return a naked or hidden single without trying possibilities."""
        candidates = {(r, c): cls._candidates(grid, r, c)
                      for r in range(9) for c in range(9) if grid[r][c] == 0}
        for cell, values in candidates.items():
            if len(values) == 1:
                return (*cell, next(iter(values)))

        units = []
        units.extend([[(r, c) for c in range(9)] for r in range(9)])
        units.extend([[(r, c) for r in range(9)] for c in range(9)])
        units.extend([[(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3)]
                      for br in range(0, 9, 3) for bc in range(0, 9, 3)])
        for unit in units:
            for value in range(1, 10):
                places = [(r, c) for r, c in unit if value in candidates.get((r, c), set())]
                if len(places) == 1:
                    return (*places[0], value)
        return None

    @classmethod
    def _is_logically_solvable(cls, puzzle: List[List[int]]) -> bool:
        grid = [row[:] for row in puzzle]
        while True:
            move = cls._next_logical_move(grid)
            if move is None:
                return all(all(value for value in row) for row in grid)
            row, col, value = move
            grid[row][col] = value

    @classmethod
    def _solution_count(cls, puzzle: List[List[int]], limit: int = 2) -> int:
        grid = [row[:] for row in puzzle]

        def solve() -> int:
            best = None
            best_values = None
            for r in range(9):
                for c in range(9):
                    if grid[r][c] == 0:
                        values = cls._candidates(grid, r, c)
                        if not values:
                            return 0
                        if best_values is None or len(values) < len(best_values):
                            best, best_values = (r, c), values
            if best is None:
                return 1
            total = 0
            r, c = best
            for value in best_values:
                grid[r][c] = value
                total += solve()
                if total >= limit:
                    break
            grid[r][c] = 0
            return total

        return solve()

    def remove_numbers(self, difficulty: str = "MEDIUM") -> bool:
        """
        Remove numbers from the board based on difficulty level.
        
        Args:
            difficulty: "EASY", "MEDIUM", or "HARD" (case-insensitive)
        """
        # Normalize difficulty to uppercase
        difficulty = difficulty.upper()
        
        # Get cells to remove from difficulty map
        cells_to_remove = self.DIFFICULTY_LEVELS.get(difficulty, 45)
        
        removed = 0
        cells = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(cells)
        for row, col in cells:
            if removed >= cells_to_remove:
                break
            value = self.board[row][col]
            self.board[row][col] = 0
            if self._solution_count(self.board) == 1 and self._is_logically_solvable(self.board):
                removed += 1
            else:
                self.board[row][col] = value
        return removed >= cells_to_remove
