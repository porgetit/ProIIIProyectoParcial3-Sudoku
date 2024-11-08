# Sudoku Solver Project

Este proyecto consiste en la implementación de un solucionador de Sudoku en Python, usando técnicas avanzadas de resolución de restricciones como *backjumping* y propagación de restricciones. El proyecto fue desarrollado como entrega para el parcial 3 del curso **Programación 3**, **Grupo 1** de la **carrera de Ingeniería de Sistemas y Computación** de la **Universidad Tecnológica de Pereira**, en el **semestre 2024-2**, bajo la dirección del profesor **Ramiro Andrés Barrios Valencia**. Escrito por **Kevin Esguerra Cardona**.

## Descripción de Clases

### `Var`
La clase `Var` representa una celda del tablero de Sudoku con su respectivo dominio de posibles valores. Implementa métodos para la asignación y administración del dominio de cada variable:
- **location** (`Tuple[int, int]`): Coordenadas de la variable en el tablero.
- **domain** (`List[int]`): Valores posibles para la variable.
- **previous_domains** (`List[List[int]]`): Historial de dominios previos, útil para restaurar valores tras fallos en asignaciones.

**Métodos principales**:
- `assign_value(value: int)`: Asigna un valor específico si pertenece al dominio.
- `reset_domain(failed_value: int = None)`: Restaura el dominio al estado anterior o al inicial, excluyendo el valor que causó el fallo si es necesario.
- `is_assigned() -> bool`: Verifica si la variable está asignada (dominio de longitud 1).
- `get_value() -> int`: Obtiene el valor asignado.

### `SudokuBoard`
La clase `SudokuBoard` modela el tablero de Sudoku y su lógica de restricciones. Crea una matriz 9x9 de objetos `Var`, permitiendo asignar valores iniciales y aplicar reglas de restricción en filas, columnas y subgrillas.

**Métodos principales**:
- `propagate_constraints()`: Aplica restricciones en todo el tablero.
- `remove_values(row: int, col: int, value: int)`: Elimina un valor asignado de los dominios de celdas en la misma fila, columna o subgrilla.
- `apply_naked_pairs()`: Detecta y aplica la regla de pares desnudos en filas, columnas y subgrillas.
- `assign_value(row: int, col: int, value: int)`: Asigna un valor a una celda y propaga restricciones.
- `get_unassigned_values() -> List[Tuple[int, int]]`: Obtiene las coordenadas de las celdas no asignadas.

### `SudokuValidator`
`SudokuValidator` verifica si una solución de Sudoku es válida. Evalúa el cumplimiento de las reglas de filas, columnas y subgrillas.

**Métodos principales**:
- `is_valid(board: SudokuBoard) -> bool`: Comprueba la validez del tablero completo.
- Métodos auxiliares para validar filas (`_validate_rows`), columnas (`_validate_columns`) y subgrillas (`_validate_subgrids`).

### `SudokuSolver`
Esta clase implementa el algoritmo de resolución utilizando *backjumping*. Toma un objeto `SudokuBoard` y resuelve el tablero aplicando técnicas de resolución y retroceso.

**Métodos principales**:
- `solve() -> bool`: Dispara el algoritmo de resolución.
- `backjumping_solve(row: int = 0, col: int = 0) -> bool`: Implementa el algoritmo de *backjumping*.
- `find_conflicting_var(conflicts, row, col) -> Tuple`: Identifica la variable que causó un conflicto en la asignación.

### `Tester`
Clase auxiliar que facilita las pruebas del algoritmo de solución sobre una lista de tableros de Sudoku.

**Métodos principales**:
- `string_to_board(input: str) -> List[List[int]]`: Convierte una cadena de enteros en una matriz 9x9.
- `pboard(board: SudokuBoard)`: Imprime el estado actual del tablero.
- `play()`: Ejecuta pruebas en cada tablero proporcionado en la lista.

## Problema Conocido en la Solución

El algoritmo implementado (*backjumping*) es efectivo en algunos casos y ha sido capaz de resolver satisfactoriamente 5 de los ejemplos propuestos. Sin embargo, falla en muchos otros casos, posiblemente debido a una implementación limitada o a un problema desconocido en el código. A pesar de estos inconvenientes, el algoritmo es estable en comparación con métodos como Monte Carlo. Aunque no garantiza una solución en el 100% de los casos, se ha decidido usarlo para esta entrega.

Soy consciente de las limitaciones de esta implementación. Llevo más de una semana trabajando diariamente en el proyecto sin alcanzar una efectividad completa. Como siguiente paso, probaré algoritmos de resolución más lentos pero con mayor efectividad, como los algoritmos genéticos, aprovechando su capacidad de paralelización, o resolver con algoritmos híbridos que combinen las mejores características de varias técnicas para aumentar la precisión y la eficiencia.

## Documentos externos
- `commands.txt` instrucciones para exportar e importar el entorno de trabajo junto con sus distintos requistos.
- `entorno.yml` entorno de anaconda sobre el que se ha construido el proyecto.
- `requirements.txt` listado de requisitos de python listo para importar con el comando `pip install -r requirements.txt`
