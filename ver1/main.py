import argparse
from board import SudokuBoard
from solver import SudokuSolverMCTS, SudokuSolverChronologicalBackTracking
from tqdm import tqdm

def generate_boards(num_boards, difficulty, save_to=None):
    boards = []
    for _ in tqdm(range(num_boards), desc="Generando tableros"):
        boards.append(SudokuBoard(difficulty=difficulty))
    if save_to:
        with open(save_to, 'w') as file:
            for board in tqdm(boards, desc="Guardando tableros generados"):
                flat_board = [cell.assigned_value or 0 for row in board.grid for cell in row]
                file.write(''.join(map(str, flat_board)) + '\n')
    return boards

def solve_boards(boards, algorithm, save_to=None):
    flat_solutions = []
    solutions = []    
    for board in tqdm(boards, desc="Solucionando"):
        solver = algorithm(board)
        if solver.solve():
            solutions.append(board)
            flat_solutions.append([board.grid[i][j].assigned_value for i in range(9) for j in range(9)])
    if save_to:
        with open(save_to, 'w') as file:
            for solution in tqdm(flat_solutions, desc="Guardando respuestas"):
                file.write(''.join(map(str, solution)) + '\n')
    return solutions

def load_boards_from_file(file_path):
    boards = []
    with open(file_path, 'r') as file:
        for line in file:
            # Convierte la línea en una lista de enteros
            flat_board = list(map(int, line.strip()))
            # Reorganiza flat_board en una estructura 9x9
            board_values = [flat_board[i * 9:(i + 1) * 9] for i in range(9)]
            # Crea una instancia de SudokuBoard con la estructura 9x9
            board = SudokuBoard(initial_values=board_values)
            boards.append(board)
    return boards

# def print(board: SudokuBoard):
#     for i in range(9):
#         for j in range(9):
#             print(board.grid[i][j])
#         print('\n')

def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver CLI")
    
    # Required arguments for primary functions
    subparsers = parser.add_subparsers(dest="command", help="Choose a command")
    
    # Solve boards from file
    solve_parser = subparsers.add_parser("solve", help="Solve Sudoku boards from a text file")
    solve_parser.add_argument("-i", "--input_file", type=str, help="Path to the input file containing Sudoku boards")
    solve_parser.add_argument("-o", "--output_file", type=str, help="Path to save the solved boards")
    solve_parser.add_argument("-a", "--algorithm", choices=["mcts", "backtracking"], default="mcts", 
                              help="Choose the solving algorithm (default: mcts)")

    # Generate and solve a specified number of boards
    generate_parser = subparsers.add_parser("generate", help="Generate and solve Sudoku boards")
    generate_parser.add_argument("-n", "--num_boards", type=int, help="Number of Sudoku boards to generate and solve")
    generate_parser.add_argument("-d", "--difficulty", type=int, choices=range(5), default=4, 
                                 help="Difficulty level for board generation (0: Very easy, 1: Easy, 2: Medium, 3: Hard, 4:Extreme)")
    generate_parser.add_argument("-sb", "--save_boards", type=str, help="File path to save the generated boards (default: boards.txt)")
    generate_parser.add_argument("-ss", "--save_solutions", type=str, help="File path to save the solved boards (default: solutions.txt)")
    generate_parser.add_argument("-a", "--algorithm", choices=["mcts", "backtracking"], default="mcts", 
                                 help="Choose the solving algorithm (default: mcts)")
    
    # Verbose flag for detailed output
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    
    # Verbose option
    verbose = True

    if args.command == "solve":
        if verbose:
            print(f"Loading boards from {args.input_file}")
        
        # Load boards
        boards = load_boards_from_file(args.input_file)
        
        # Select algorithm
        if args.algorithm == "mcts":
            algorithm = SudokuSolverMCTS
        else:
            algorithm = SudokuSolverChronologicalBackTracking
        
        # Solve boards
        if verbose:
            print("Solving boards...")
        solve_boards(boards, algorithm, save_to=args.output_file)
        if verbose and args.output_file:
            print(f"Solutions saved to {args.output_file}")

    elif args.command == "generate":
        if verbose:
            print(f"Generating {args.num_boards} boards with difficulty {args.difficulty}")
        
        # Generate boards
        boards = generate_boards(args.num_boards, args.difficulty, save_to=args.save_boards)
        
        # Select algorithm
        if args.algorithm == "mcts":
            algorithm = SudokuSolverMCTS
        else:
            algorithm = SudokuSolverChronologicalBackTracking
        
        # Solve boards
        if verbose:
            print("Solving generated boards...")
        solutions = solve_boards(boards, algorithm, save_to=args.save_solutions)

        if verbose:
            for board in boards:
                temp_board = [[board.grid[i][j].assigned_value if board.grid[i][j].assigned_value else 0 for j in range(9)] for i in range(9)]
                for row in temp_board:
                    print(row)
                print('-'*27)
        if verbose:
            for solution in solutions:
                temp_solution = [[solution.grid[i][j].assigned_value if solution.grid[i][j] else 0 for j in range(9) for i in range(9)]]
                for row in temp_solution:
                    print(row)
                print('-'*27)
            
        
        if verbose:
            if args.save_boards:
                print(f"Generated boards saved to {args.save_boards}")
            if args.save_solutions:
                print(f"Solutions saved to {args.save_solutions}")

if __name__ == "__main__":
    main()