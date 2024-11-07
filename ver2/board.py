from var import Var
from typing import List

class SudokuBoard:
    
    def __init__(self, initial_values: List[List[int]] = None):
        """`IMPORTANTE` debo verificar que los valores de entrada sean 81
        """
        initial_values = initial_values if initial_values else [[0 for _ in range(9)] for _ in range(9)]
        self.grid = [[Var((i, j), {initial_values[i][j]} if initial_values[i][j] else set(range(1,10))) for j in range(9)] for i in range(9)]
        self.propagate_constraints()
        
        
    def var(self, row: int, col: int) -> Var:
        """Este método permite obtener rápida y cómodamente el objeto Var almacenado en una ubicación dada del tablero.

        Args:
            row (int): fila.
            col (int): columna.
            
        Raises:
            IndexError: Error en caso de ingresar coordenadas inválidas como números negativos o mayores a 8.

        Returns:
            Var: Objeto Var almacenado en la ubicación dada.
        """
        try:            
            return self.grid[row][col]
        except IndexError:
            raise IndexError(f"No existe la posición ({row},{col})")
        
        
    def propagate_constraints(self) -> None:
        """Este método propaga las restricciones de valor en filas, columnas y subcuadrículas.
        """
        for row in range(9):
            for col in range(9):
                if self.var(row, col).is_assigned():
                    self.remove_values(row, col, self.var(row, col).get_value())
                    
    
    def remove_values(self, row: int, col: int, value: int) -> None:
        """Método auxiliar de `propagate_constraints` que dirige la propagación de las restricciones.
        
        Args:
            row (int): fila de la variable asignada (que contiene el valor a eliminar).
            col (int): columna de la variable asignada (que contiene el valor a eliminar).
            value (int): valor a eliminar.
        """
        self._by_row_column(row, col, value)
        self._by_subgrid(row, col, value)
            
                
    def _by_row_column(self, row: int, col: int, value: int) -> None:
        """Método auxiliar de `remove_values` que se encarga de restringir los dominios de las variables afectadas en filas y columnas.

        Args:
            row (int): fila a ser afectada.
            col (int): columna a ser afectada.
            value (int): valor a ser eliminado de los dominios de las variables afectadas por la restricción.

        Raises:
            RuntimeError: Ocurre cuando se viola una restricción, sea por fila o columna. 
            Esta excepción está cargada con una lista que contiene dos tuplas, la primera son las coordenadas de la variable evaluada
            y la segunda son las coordenadas de la variable con quien entra en conflicto.
        """
        for i in range(9):
            if not self.var(row, i).is_assigned() and i != col:
                try:
                    self.var(row, i).domain.remove(value)
                except ValueError:
                    pass
            if not self.var(i, col).is_assigned() and i != row:
                try:
                    self.var(i, col).domain.remove(value)
                except ValueError:
                    pass
            
            if self.var(row, i).is_assigned() and i != col and self.var(row, i).get_value() == value:
                raise RuntimeError([(row, col), (row, i)])
            if self.var(i, col).is_assigned() and i != row and self.var(i, col).get_value() == value:
                raise RuntimeError([(row, col), (i, col)])
    
            
    def _by_subgrid(self, row: int, col: int, value: int) -> None:
        """Método auxiliar de `remove_values` que se encarga de restringir los dominios de las variables afectadas en subcuadrículas.

        Args:
            row (int): fila a ser afectada.
            col (int): columna a ser afectada.
            value (int): valor a ser eliminado de los dominios de las variables afectadas por la restricción.

        Raises:
            RuntimeError: Ocurre cuando se viola una restricción por subcuadrícula.
            Esta excepción está cargada con una lista que contiene dos tuplas, la primera son las coordenadas de la variable evaluada
            y la segunda son las coordenadas de la variable con quien entra en conflicto.
        """
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for subrow in range(start_row, start_row + 3):
            for subcol in range(start_col, start_col + 3):
                if not self.var(subrow, subcol).is_assigned() and row != subrow and col != subcol:
                    try:
                        self.var(subrow, subcol).domain.remove(value)
                    except ValueError:
                        pass
                if self.var(subrow, subcol).is_assigned() and row != subrow and col != subcol and self.var(subrow, subcol).get_value() == value:
                    raise RuntimeError([(row, col), (subrow, subcol)])
                
                
    def assign_value(self, row: int, col: int, value: int) -> None:
        """Este método permite asignar de forma segura un valor a una variable teniendo en cuenta las restricciones impuestas.

        Args:
            row (int): coordenada de la fila de la variable a modificar.
            col (int): coordenada de la columna de la variable a modificar.
            value (int): valor a asignar a la variable que se quiere modificar.

        Raises:
            ValueError: Se dispara en `Var.assig_value()` cuando se quiere asignar un valor a una variable y este no se encuentra dentro de su dominio.
            RuntimeError: Se dispara cuando se viola una restricción en `propagate_constraints`.
        """
        try:
            self.var(row, col).assign_value(value)
            self.propagate_constraints()
        except ValueError:
            raise ValueError([(row, col, value)])
        except RuntimeError as r:
            raise RuntimeError(r.args[0])
        