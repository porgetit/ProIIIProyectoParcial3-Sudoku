from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Var:
    """Esta clase representa una variable/casilla del tablero
    """
    location: Tuple[int, int]
    domain: List[int]
    
    def assign_value(self, value: int) -> None:
        """Este método permite asignar un valor a la variable

        Args:
            value (int): valor a ser asignado
            verbose (bool): parámetro de extensión de contexto

        Raises:
            ValueError: Ocurre al intentar asignar un valor inválido a una variable.
            Un valor inválido es aquel que no se encuentra dentro del dominio actual de la variable.
        """
        if value in self.domain:
            self.domain = [value]
        else:
            raise ValueError()
    
    def reset_domain(self, verbose: bool) -> None:
        """Este método permite reiniciar rápidamente el dominio de la variable

        Args:
            verbose (bool): parámetro de extensión de contexto
        """
        self.domain = list(range(1,10))
        if verbose:
            print(f"Dominio de Var{self.location} reiniciado")
            
    def is_assigned(self) -> bool:
        """Este método permite comprobar rápidamente si la variable ya tiene un único valor asignado

        Returns:
            bool: True quiere decir que la variable tiene un único valor asignado.
        """
        return True if len(self.domain) == 1 else False
        
    def get_value(self) -> int:
        """Este método permite obtener rápidamente el valor asignado a la variable si es que esta esta asignada

        Raises:
            RuntimeError: Salta cuando se intenta obtener el valor de una variable no asignada

        Returns:
            int: valor asignado a la variable
        """
        if not self.is_assigned():
            raise RuntimeError(f"La variable {self.location} aún no es asignada")
        
        return self.domain[0]