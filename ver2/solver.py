from board import SudokuBoard

class ChronoBacktrack:
    """Esta clase encapsula el solucionador de sudokus por Backtracking Chronológico
    """
    
    def __init__(self, board: SudokuBoard) -> None:
        self.board = board
        
    def solve(self) -> None:
        unassigned_vars = self.board.get_unassigned_vars()
        if not unassigned_vars:
            return None
        
        row, col = unassigned_vars[0]
        
        for value in self.board.var(row, col).domain:
            try:
                self.board.assign_value(row, col, value)
            except ValueError:
                raise ValueError(f"Error al asignar el valor {value} a ({row},{col})")
            except RuntimeError:
                pass
            
            if self.solve():
                return None
        
            self.board.var(row, col).reset_domain()
            self.board.propagate_constraints()
            
        raise RuntimeError()
            