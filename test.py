from generator import SudokuGenerator

gen = SudokuGenerator()

board = gen.generate("MEDIUM")

for row in board:
    print(row)
