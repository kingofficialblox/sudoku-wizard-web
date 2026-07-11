from generator import SudokuGenerator

gen = SudokuGenerator()

board = gen.generate("medium")

for row in board:
    print(row)
