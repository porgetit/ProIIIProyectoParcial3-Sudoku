from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class Var:
    """Esta clase contiene la estructura y funcionalidad básica para una variable del tablero de sudoku.
    
    Args:
        location (Tuple[int, int]): coordenadas de la variable en el tablero de sudoku.
        domain (List[int]): dominio (a.k.a posibles valores) de la variable.
        previous_domains (List[List[int]], optional): historial de todos los dominios que ha tenido la variable. Este campo normalmente no es requerido y simplemente sirve para uso interno del resolutor.
    """
    location: Tuple[int,  int]
    domain: List[int]
    previous_domains: List[List[int]] = field(default_factory=list)
    
    def assign_value(self, value: int) -> None:
        """Método que permite asignar un valor a la variable.

        Args:
            value (int): valor a asignar a la variable.

        Raises:
            ValueError: Ocurre si el valor que se quiere asignar no está dentro del dominio de la variable.
        """
        if value in self.domain:
            self.previous_domains.append(self.domain[:])
            self.domain = [value]
        else:
            raise ValueError()
        
    def reset_domain(self, failed_value: int = None) -> None:
        """Método que permite reestablecer el dominio de la variable.

        Args:
            failed_value (int, optional): Valor que ha fallado y no será incluido en el nuevo dominio de la variable. Defaults to None.
        """
        if self.previous_domains:
            self.domain = self.previous_domains.pop()
            if failed_value and failed_value in self.domain:
                self.domain.remove(failed_value)
        else:
            self.previous_domains.append(self.domain[:])
            self.domain = list(range(1,10))
            
    def is_assigned(self) -> bool:
        """Método que retorna si la variable esta o no asignada. Una variable se considera asignada cuando su dominio es de longitud 1.

        Returns:
            bool: True si la variable esta asignada, False en caso contrario.
        """
        return True if len(self.domain) == 1 else False
    
    def get_value(self) -> int:
        """Método que permite obtener el valor asignado de una variable.

        Raises:
            RuntimeError: Ocurre al intentar obtener un valor de una variable que no está asignada.

        Returns:
            int: valor asignado a la variable.
        """
        if not self.is_assigned():
            raise RuntimeError()
        
        return self.domain[0]
    
    def set_domain(self, domain: List[int]) -> None:
        """Método para establecer un dominio de manera precisa en una variable.

        Args:
            domain (List[int]): nuevo dominio.
        """
        self.previous_domains.append(self.domain[:])
        self.domain = domain
        
class SudokuBoard:
    """Clase que representa un tablero de Sudoku."""
    
    def __init__(self, initial_values: List[List[int]] = None, verbose: bool = False):
        """Constructor

        Args:
            initial_values (List[List[int]], optional): valores con los que será construido el tablero. Defaults to None. Por defecto se creará un tablero vacío.
            verbose (bool, optional): Si es True, se activará el modo verbose. Defaults to False.
        """
        self.verbose = verbose
        initial_values = initial_values if initial_values else [[0 for _ in range(9)] for _ in range(9)]
        self.grid = [[Var((row, col), [initial_values[row][col]] if initial_values[row][col] else list(range(1, 10))) for col in range(9)] for row in range(9)]
        self.propagate_constraints()
    
    def var(self, row: int, col: int) -> Var:
        """Método que devuelve el objeto Var almacenado en una posición dada.

        Args:
            row (int): coordenada de fila.
            col (int): coordenada de columna.

        Returns:
            Var: Objeto almacenado en las coordenadas dadas.
        """
        try:
            return self.grid[row][col]
        except IndexError:
            return None
        
    def propagate_constraints(self) -> None:
        """Método encargado de propagar de forma recursiva las restricciones de fila, columna, subgrilla y pares."""
        changes = True
        while changes:
            changes = False
            for row in range(9):
                for col in range(9):
                    if self.var(row, col).is_assigned():
                        if self.remove_values(row, col, self.var(row, col).get_value()):
                            changes = True
                            if self.verbose:
                                print(f"Propagando desde ({row}, {col}): valor {self.var(row, col).get_value()}")
            if self.apply_naked_pairs():
                changes = True
                
    def remove_values(self, row: int, col: int, value: int) -> bool:
        """Método que llama a los métodos de restricciones por filas, columnas y subgrilla."""
        changed = self._by_row_column(row, col, value) or self._by_subgrid(row, col, value)
        return changed
    
    def _by_row_column(self, row: int, col: int, value: int) -> bool:
        """Elimina el valor asignado a una variable en (row, col) de las variables relacionadas por fila y columna."""
        changed = False
        for i in range(9):
            if not self.var(row, i).is_assigned() and i != col:
                if value in self.var(row, i).domain:
                    self.var(row, i).domain.remove(value)
                    changed = True
                    if self.verbose:
                        print(f"Eliminando {value} de la fila {row}, columna {i}")
            if not self.var(i, col).is_assigned() and i != row:
                if value in self.var(i, col).domain:
                    self.var(i, col).domain.remove(value)
                    changed = True
                    if self.verbose:
                        print(f"Eliminando {value} de la fila {i}, columna {col}")
            
            if self.var(row, i).is_assigned() and i != col and self.var(row, i).get_value() == value:
                raise RuntimeError([(row, col), (row, i)])
            if self.var(i, col).is_assigned() and i != row and self.var(i, col).get_value() == value:
                raise RuntimeError([(row, col), (i, col)])
        
        return changed
    
    def _by_subgrid(self, row: int, col: int, value: int) -> bool:
        """Elimina el valor asignado a una variable en (row, col) de las variables relacionadas por subcuadrícula."""
        changed = False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for subrow in range(start_row, start_row + 3):
            for subcol in range(start_col, start_col + 3):
                if not self.var(subrow, subcol).is_assigned() and subrow != row and subcol != col:
                    if value in self.var(subrow, subcol).domain:
                        self.var(subrow, subcol).domain.remove(value)
                        changed = True
                        if self.verbose:
                            print(f"Eliminando {value} de la subcuadrícula ({subrow}, {subcol})")
                
                if self.var(subrow, subcol).is_assigned() and subrow != row and subcol != col and self.var(subrow, subcol).get_value() == value:
                    raise RuntimeError([(row, col), (subrow, subcol)])
        
        return changed
    
    def apply_naked_pairs(self) -> bool:
        """Aplica la regla de dominios pares en filas, columnas y subcuadrículas."""
        changed = False
        for row in range(9):
            changed |= self._naked_pairs_in_unit([self.var(row, col) for col in range(9)])
            
        for col in range(9):
            changed |= self._naked_pairs_in_unit([self.var(row, col) for row in range(9)])
            
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                subgrid = [self.var(start_row + i, start_col + j) for i in range(3) for j in range(3)]
                changed |= self._naked_pairs_in_unit(subgrid)
        
        return changed
    
    def _naked_pairs_in_unit(self, unit: List[Var]) -> bool:
        """Aplica la regla de dominios pares a una unidad dada (fila, columna o subcuadrícula)."""
        changed = False
        pairs = [var for var in unit if len(var.domain) == 2]
        pair_domains = [var.domain for var in pairs]
        
        for i in range(len(pair_domains)):
            for j in range(i + 1, len(pair_domains)):
                if pair_domains[i] == pair_domains[j]:
                    pair_values = pair_domains[i]
                    
                    for var in unit:
                        if var.domain != pair_values and not var.is_assigned():
                            for value in pair_values:
                                if value in var.domain:
                                    var.domain.remove(value)
                                    changed = True
                                    if self.verbose:
                                        print(f"Aplicando naked pair {pair_values} en unidad, eliminando {value} de {var.location}")
        
        return changed
    
    def assign_value(self, row: int, col: int, value: int) -> None:
        """Método para asignar un valor dado a una variable en las coordenadas dadas.

        Args:
            row (int): coordenada de fila.
            col (int): coordenada de columna.
            value (int): valor a asignar.

        Raises:
            ValueError: Ocurre en Var.assign_value cuando se intenta asignar un valor fuera del dominio de esta.
            RuntimeError: Ocurre en propagate_constraints cuando se viola alguna restricción establecida.
        """
        try:
            self.var(row, col).assign_value(value)
            self.propagate_constraints()
        except ValueError:
            raise ValueError()
        except RuntimeError as r:
            raise RuntimeError(r.args[0])
        finally:
            if not self.var(row, col).is_assigned():
                self.var(row, col).reset_domain()
                
    def get_unassigned_values(self) -> List[Tuple[int, int]]:
        """Método que retorna una lista con las coordenadas de las variables que no se han asignado. Normalmente, se necesitan conocer para evitar modificar las pistas originales del tablero.

        Returns:
            List[Tuple[int, int]]: Estructura que contiene las coordenadas de cada una de las variables que no han sido asignadas.
        """
        return [(row, col) for col in range(9) for row in range(9) if not self.var(row, col).is_assigned()]
   
class SudokuValidator:
    """Clase que encapsula la lógica para verificar las soluciones obtenidas.
    """
    
    @staticmethod
    def is_valid(board: SudokuBoard) -> bool:
        """Método que aplicar las reglas de fila, columna y subcuadrícula para verificar que la solución dada sea válida.

        Args:
            board (SudokuBoard): Objeto que representa el tablero resuelto que debe ser verificado.

        Returns:
            bool: True si el tablero `board` es válido. False en caso contrario.
        """
        return (SudokuValidator._validate_rows(board) and
                SudokuValidator._validate_columns(board) and
                SudokuValidator._validate_subgrids(board))
        
    @staticmethod
    def _validate_rows(board: SudokuBoard) -> bool:
        """Método que valida la regla de filas.

        Args:
            board (SudokuBoard): Objeto que representa el tablero resuelto que debe ser verificado.

        Returns:
            bool: True si el tablero `board` es válido. False en caso contrario.
        """
        for row in range(9):
            seen = set()
            for col in range(9):
                value = board.var(row, col).get_value()
                if value != 0:
                    if value in seen:
                        return False
                    seen.add(value)
        
        return True
    
    @staticmethod
    def _validate_columns(board: SudokuBoard) -> bool:
        """Método que valida la regla de columnas.

        Args:
            board (SudokuBoard): Objeto que representa el tablero resuelto que debe ser verificado.

        Returns:
            bool: True si el tablero `board` es válido. False en caso contrario.
        """
        for col in range(9):
            seen = set()
            for row in range(9):
                value = board.var(row, col).get_value()
                if value != 0:
                    if value in seen:
                        return False
                    seen.add(value)
                    
        return True
    
    @staticmethod
    def _validate_subgrids(board: SudokuBoard) -> bool:
        """Método que valida la regla de subcuadrículas.

        Args:
            board (SudokuBoard): Objeto que representa el tablero resuelto que debe ser verificado.

        Returns:
            bool: True si el tablero `board` es válido. False en caso contrario.
        """
        for start_row in range(0, 9 ,3):
            for start_col in range(0, 9, 3):
                seen = set()
                for row in range(start_row, start_row+3):
                    for col in range(start_col, start_col+3):
                        value = board.var(row, col).get_value()
                        if value != 0:
                            if value in seen:
                                return False
                            seen.add(value)
                            
        return True
    
class SudokuSolver:
    """Clase que encapsula la lógica del resolutor."""
    
    def __init__(self, board: SudokuBoard, verbose: bool = False):
        """Constructor

        Args:
            board (SudokuBoard): tablero que debe ser resuelto.
            verbose (bool, optional): Si es True, se activará el modo verbose. Defaults to False.
        """
        self.board = board
        self.verbose = verbose
        self.conflict_tracker = {}
        
    def solve(self) -> bool:
        """Método que sirve para disparar el algoritmo de resolución y controlar el flujo en caso de excepciones.

        Returns:
            bool: True el tablero fue solucionado. False caso contrario.
        """
        try:
            return self.backjumping_solve()
        except RuntimeError:
            if self.verbose:
                print("Se ha detectado un conflicto que no puede ser resuelto.")
            return False
        
    def backjumping_solve(self, row: int = 0, col: int = 0) -> bool:
        """Método que resuelve un tablero dado usando el algoritmo de backjumping.

        Returns:
            bool: True el tablero fue solucionado. False caso contrario.
        """
        unassigned_vars = self.board.get_unassigned_values()
        if not unassigned_vars:
            if self.verbose:
                print("El tablero ha sido resuelto exitosamente.")
            return True
        
        row, col = unassigned_vars[0]
        
        for value in self.board.var(row, col).domain:
            if self.verbose:
                print(f"Intentando asignar {value} a la celda ({row}, {col})")
            
            try:
                self.board.assign_value(row, col, value)
                if self.backjumping_solve(row, col):
                    return True
            except RuntimeError as conflict:
                conflicting_cell = self.find_conflicting_var(conflict.args[0], row, col)
                if self.verbose:
                    print(f"Conflicto detectado en ({row}, {col}) con {conflict.args[0]}. Intentando retroceder a {conflicting_cell}.")
                if conflicting_cell:
                    self.board.var(row, col).reset_domain()
                    self.board.propagate_constraints()
                    return self.backjumping_solve(*conflicting_cell)
            
            if self.verbose:
                print(f"Restableciendo dominio de la celda ({row}, {col}) y propagando restricciones.")
            self.board.var(row, col).reset_domain()
            self.board.propagate_constraints()
        
        if self.verbose:
            print(f"No se encontró solución al intentar asignar valores a la celda ({row}, {col}). Retrocediendo.")
        return False
    
    def find_conflicting_var(self, conflicts, row, col) -> Tuple:
        """Método que encuentra las variables que entran en conflicto con la que está en una posición dada.

        Returns:
            Tuple: Lista de variable (coordenadas) que causan conflicto.
        """
        for conflict in conflicts:
            if conflict != (row, col):
                self.conflict_tracker[(row, col)] = conflict
        
        if self.verbose:
            print(f"Conflictos registrados para la celda ({row}, {col}): {conflicts}")
        
        return self.conflict_tracker.get((row, col), None)
  
@dataclass
class Tester:
    """Clase de pruebas.
    """
    sudokus: List[str]
    algorithm: type
    solved_boards: List[SudokuBoard] = field(default_factory=list)
    
    def string_to_board(self, input: str) -> List[List[int]]:
        """Método que toma una cadea de enteros y trata de convertirla en un input válido para la clase `SudokuBoard`.

        Args:
            input (str): cadena de enteros dada.

        Returns:
            List[List[int]]: tablero representado en un formato válido.
        """
        return [[int(input[i*9+j]) for j in range(9)] for i in range(9)]
    
    def pboard(self, board: SudokuBoard) -> None:
        """Método que toma un tablero `SudokuBoard` y lo imprime en pantalla.

        Args:
            board (SudokuBoard): tablero a imprimir.
        """
        for row in [[board.var(row, col).get_value() if board.var(row, col).is_assigned() else 0 for col in range(9)] for row in range(9)]:
            print(row)
        print('\n')
            
    def play(self) -> None:
        """Método que ejecuta el script de prueba sobre cada tablero dado.
        
        1. Obtención de valores iniciales.
        2. Creación del objeto `SudokuBoard`.
        3. Creación del objeto resolutor.
        4. Intenter resolver el tablero.
        
        """
        for chain in self.sudokus:
            initial_values = self.string_to_board(chain)
            board = SudokuBoard(initial_values)
            solver = self.algorithm(board)
            try:
                if solver.solve() and SudokuValidator.is_valid(solver.board):
                    self.solved_boards.append(solver.board)
                else:
                    pass
            except RuntimeError:
                print("\nError: No se pudo solucionar el tablero debido a una violación de restricciones.")
                
sudokus = [
    "000000000500090000030506400903050020080009500600001003009000300000060281200000605",
    "200000400008000050009004000000060040096500080087093000905030008060007025070080000",
    "000705200000002976001000004040010090000000001102080605000576000080000009400000060",
    "040001803300070600001000050900050000000900705080700300800000019000060030070094500",
    "000006008010000320030070619001000087060020000308090000650900003080000000200000700",
    "090001000400000007070392014009000560007605003300400702000000000032006000060027100",
    "100000000030040050000007200000000060200000300000080000070000004600000000000500001"
]


tester = Tester(sudokus=sudokus, algorithm=SudokuSolver)
tester.play()
for board in tester.solved_boards:
    tester.pboard(board=board)
print(f"Se han resuelto {len(tester.solved_boards)} de {len(sudokus)} tableros")
