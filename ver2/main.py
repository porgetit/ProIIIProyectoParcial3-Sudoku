from generator import BoardGenerator
from solver import ChronoBacktrack
from board import SudokuBoard

def pboard(board: SudokuBoard) -> None:
    for row in [[board.var(row, col).get_value() if board.var(row, col).is_assigned() else 0 for col in range(9)] for row in range(9)]:
        print(row)

board = BoardGenerator(0).generate()
pboard(board)
    
solver = ChronoBacktrack(board)
try:
    solver.solve()
    pboard(solver.board)
except RuntimeError:
    print("No se pudo solucionar el tablero")
    
