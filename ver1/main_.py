from board import SudokuBoard
from solver import SudokuSolverMCTS
from tqdm import tqdm

ITS = 1000
boards = []

for i in tqdm(range(ITS), desc="Generando tableros"):
    board = SudokuBoard(difficulty=4)
    boards.append(board)

for board in tqdm(boards, desc="Resolviendo por MCTS"):
    solver = SudokuSolverMCTS(board)
    solver.solve()