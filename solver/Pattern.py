from solver.Entity import Entity
from solver.Logic import *


class Pattern(Producting):
    def __init__(self, axiom: str, pattern: str):
        self._axiom = axiom
        self._pattern = "{}.{}".format(axiom, pattern)

        self._base_logic = And(self._axiom, self._pattern)

    def product(self, entity: Entity) -> bool:
        return self._base_logic.product(entity)

    def conflicts_with(self, entity: Entity) -> bool:
        pass

