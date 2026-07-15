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
        # Reset board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill complete solution
        self.fill_board()
        
        # Save the complete solution
        self.solution = [row[:] for row in self.board]
        
        # Remove numbers based on difficulty
        self.remove_numbers(difficulty)
        
        return self.board

    def remove_numbers(self, difficulty: str = "MEDIUM") -> None:
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
        
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1
