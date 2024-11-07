from board import SudokuBoard
from var import Var
from typing import Optional
import random

class SudokuSolverChronologicalBackTracking:
    '''
    Esta versión del solucionador usa el algoritmo de backtracking cronológico
    '''
    def __init__(self, board: SudokuBoard):
        self.board = board

    def solve(self) -> bool:
        unassigned_vars = self.board.get_unassigned_variables()
        if not unassigned_vars:
            return True  # Solution found

        var = unassigned_vars[0]
        row, col = var.location

        for value in var.domain:
            if self.board.is_valid_assignment(row, col, value):
                var.assign_value(value)
                self.board.propagate_constraints()

                if self.solve():
                    return True

                # Backtrack
                var.reset()
                self.board.propagate_constraints()

        return False  # Trigger backtracking

class SudokuSolverMCTS:
    def __init__(self, board: SudokuBoard, simulations: int = 100) -> None:
        self.board = board
        self.simulations = simulations

    def solve(self) -> bool:
        """Intenta resolver el Sudoku usando Monte Carlo Tree Search."""
        while not self.is_complete():
            # Encuentra las celdas no asignadas
            unassigned_vars = self.board.get_unassigned_variables()
            if not unassigned_vars:
                break

            # Selecciona una celda para probar valores
            var = unassigned_vars[0]
            best_value = self.monte_carlo_simulation(var)
            if best_value is None:
                return False  # No se encontró solución

            # Asigna el mejor valor encontrado
            var.assign_value(best_value)

        return self.is_complete()  # Retorna True si se resolvió el Sudoku

    def monte_carlo_simulation(self, var: Var) -> Optional[int]:
        """Simula varias asignaciones para una celda y elige el mejor valor."""
        domain_counts = {value: 0 for value in var.domain}

        for value in var.domain:
            for _ in range(self.simulations):
                # Asigna temporalmente el valor y verifica si el estado es factible
                var.assign_value(value)
                if self.random_simulation():
                    domain_counts[value] += 1
                var.reset()  # Revierte la asignación temporal

        # Elige el valor con mayor éxito en las simulaciones
        best_value = max(domain_counts, key=domain_counts.get, default=None)
        return best_value if domain_counts[best_value] > 0 else None

    def random_simulation(self) -> bool:
        """Realiza una simulación aleatoria completa desde el estado actual."""
        try:
            unassigned_vars = self.board.get_unassigned_variables()
            random.shuffle(unassigned_vars)
            for var in unassigned_vars:
                possible_values = list(var.domain)
                if not possible_values:
                    return False
                value = random.choice(possible_values)
                var.assign_value(value)
            return True
        finally:
            # Restablece el estado original del tablero después de la simulación
            for var in self.board.get_unassigned_variables():
                var.reset()

    def is_complete(self) -> bool:
        """Verifica si el tablero está completamente asignado."""
        return all(var.is_assigned() for row in self.board.grid for var in row)