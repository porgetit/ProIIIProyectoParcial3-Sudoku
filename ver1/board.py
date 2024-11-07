from var import Var
from typing import List, Set
import random
import numpy as np

class SudokuBoard:
    def __init__(self, difficulty: int = 4, initial_values: List[List[int]] = None):
        self.difficulty = difficulty
        initial_values = self.generate_board(difficulty) if not initial_values else initial_values
        self.grid = [
            [Var((i, j), {initial_values[i][j]} if initial_values[i][j] else set(range(1, 10)), initial_values[i][j] or None)
                for j in range(9)] for i in range(9)
        ]
        self.propagate_constraints()

    def propagate_constraints(self):
        """Aplica restricciones iniciales en el tablero en función de los valores asignados."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].is_assigned():
                    self.remove_invalid_values(i, j, self.grid[i][j].assigned_value)

    def remove_invalid_values(self, row: int, col: int, value: int):
        """Elimina un valor de las filas, columnas y subcuadrícula correspondiente."""
        for i in range(9):
            if not self.grid[row][i].is_assigned():
                self.grid[row][i].domain.discard(value)
            if not self.grid[i][col].is_assigned():
                self.grid[i][col].domain.discard(value)

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if not self.grid[i][j].is_assigned():
                    self.grid[i][j].domain.discard(value)

    def is_valid_assignment(self, row: int, col: int, value: int) -> bool:
        """Verifica si la asignación es válida en fila, columna y subcuadrícula."""
        if any(self.grid[row][j].assigned_value == value for j in range(9)):
            return False
        if any(self.grid[i][col].assigned_value == value for i in range(9)):
            return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        return all(self.grid[i][j].assigned_value != value for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3))

    def get_unassigned_variables(self) -> List[Var]:
        """Obtiene las variables no asignadas en el tablero actual."""
        return [self.grid[i][j] for i in range(9) for j in range(9) if not self.grid[i][j].is_assigned()]

    def generate_board(self, difficulty: int) -> List[List[int]]:
        """Genera el tablero inicial en función de la dificultad especificada."""
        hints = {0: (55, 65), 1: (35, 50), 2: (24, 34), 3: (17, 24), 4: (17, 17)}
        if difficulty in hints:
            return self.board_generator(random.randint(*hints[difficulty]))
        else:
            raise ValueError(f"Dificultad {difficulty} no establecida")

    def board_generator(self, hints: int) -> List[List[int]]:
        """Genera un tablero de Sudoku aleatorio con la cantidad de pistas especificada."""
        self.hints = hints
        initial_values = [[0] * 9 for _ in range(9)]
        mean, std_dev = 4, 2

        selected_positions = set()
        while len(selected_positions) < hints:
            row, col = int(np.random.normal(mean, std_dev)), int(np.random.normal(mean, std_dev))
            if 0 <= row < 9 and 0 <= col < 9:
                selected_positions.add((row, col))
        
        for row, col in selected_positions:
            valid_values = self.get_valid_values(initial_values, row, col)
            if valid_values:
                initial_values[row][col] = random.choice(list(valid_values))

        return initial_values

    def get_valid_values(self, board: List[List[int]], row: int, col: int) -> Set[int]:
        """Obtiene los valores válidos para una celda específica."""
        all_values = set(range(1, 10))
        row_values = {board[row][j] for j in range(9) if board[row][j] != 0}
        col_values = {board[i][col] for i in range(9) if board[i][col] != 0}
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        box_values = {board[r][c] for r in range(start_row, start_row + 3) for c in range(start_col, start_col + 3) if board[r][c] != 0}
        
        return all_values - row_values - col_values - box_values
