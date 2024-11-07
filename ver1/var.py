from dataclasses import dataclass
from typing import Tuple, Set, Optional

@dataclass
class Var:
    location: Tuple[int, int]
    domain: Set[int]
    assigned_value: Optional[int] = None

    def assign_value(self, value: int):
        if value in self.domain:
            self.assigned_value = value
            self.domain = {value}
        else:
            raise ValueError(f"Value {value} not in domain")

    def reset(self):
        self.domain = set(range(1, 10))
        self.assigned_value = None

    def is_assigned(self):
        return self.assigned_value is not None