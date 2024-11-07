# Sudoku CLI - Generador y Solucionador de Tableros de Sudoku

Este programa de línea de comandos (CLI) permite generar y resolver tableros de Sudoku de manera eficiente. Se pueden cargar tableros desde archivos de texto, especificar el nivel de dificultad al generar nuevos tableros y elegir entre dos algoritmos de resolución distintos. El programa también permite guardar los tableros generados y sus soluciones en archivos de texto para su posterior uso o análisis.

## Requisitos

- Python 3.6 o superior
- Dependencias adicionales: `argparse`, `tqdm` (para barras de progreso)

## Funcionalidades Principales

El programa tiene dos funcionalidades principales, accesibles a través de subcomandos:

1. **`solve`**: Resolver tableros de Sudoku a partir de un archivo de texto.
2. **`generate`**: Generar una cantidad dada de tableros de Sudoku con un nivel de dificultad especificado y resolverlos opcionalmente.

### Uso General

El formato básico para ejecutar el programa es el siguiente:

```bash
python sudoku_cli.py <comando> [opciones]
