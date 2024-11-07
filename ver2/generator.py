from board import SudokuBoard
import random
import numpy as np

class BoardGenerator:
    """Esta clase encapsula la lógica de generación de tableros de sudoku para 5 dificultades:\n
    `0` : muy fácil, entre 55 y 65 pistas\n
    `1` : fácil, entre 35 y 54 pistas\n
    `2` : medio, entre 24 y 34 pistas\n
    `3` : difícil, entre 18 y 24 pistas\n
    `4` : extremo, solo 17 pistas
    """
    
    def __init__(self, difficult: int = 4) -> None:
        """Constructor.

        Args:
            difficult (int, optional): Dificultad que se desea para el tablero. Defaults to 4.

        Returns:
            SudokuBoard: Objeto `SudokuBoard` que representa un tablero con valores iniciales.
        """
        self.difficult = difficult
    
    def generate(self) -> SudokuBoard:
        """Método auxiliar del `Constructor`. Decide una cantidad de pistas de acuerdo a la dificultad escogida.

        Raises:
            ValueError: Ocurre cuando se pasa una dificultad desconocida.

        Returns:
            SudokuBoard: Objeto `SudokuBoard` que representa un tablero con valores iniciales.
        """
        hints = {0: (55, 65), 1: (35, 54), 2: (24, 34), 3: (18, 24), 4: (17, 17)}
        if self.difficult in hints:
            return self.get_valid_board(random.randint(*hints[self.difficult]))
        else:
            raise ValueError(f"Dificultad {self.difficult} no establecida")
        
    def get_valid_board(self, hints: int) -> SudokuBoard:
        """Método auxiliar de `generate`. Genera los valores y los asigna al tablero.

        Args:
            hints (int): cantidad de valores a generar.

        Returns:
            SudokuBoard: Objeto `SudokuBoard` que representa un tablero con valores iniciales.
        """
        initial_values = [[0] * 9 for _ in range(9)]
        mean, std_dev = 4, 2

        selected_positions = []
        while len(selected_positions) < hints:
            row, col = int(np.random.normal(mean, std_dev)), int(np.random.normal(mean, std_dev))
            if 0 <= row < 9 and 0 <= col < 9:
                selected_positions.append((row, col))
                
        for pos in selected_positions:
            row, col = pos
            initial_values[row][col] = random.randint(1,9)
        
        while True:
            try:
                board = SudokuBoard(initial_values)
                return board
            except RuntimeError as e:
                row, col = e.args[0][1]
                initial_values[row][col] = random.choice([x for x in range(1, 10) if x != initial_values[row][col]])
            
        
    