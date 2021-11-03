from solver.Logic import Logic, Is, parse_logic
from solver.Entity import Entity
from solver.Exceptions import *


class Rule:
    def __init__(self, condition: [Logic, str], result: str):
        self.__condition = condition
        if not isinstance(condition, Logic):
            self.__condition = parse_logic(condition)

        self.__result = result

    @property
    def result(self):
        return self.__result

    @property
    def condition(self):
        return self.__condition

    def product(self, entity: Entity):
        try:
            if self.__condition.product(entity):
                entity.set_known(self.__result)
        except AxiomException:
            raise RuleConflictException("{} result conflicts with {} entity".format(self, entity))

    def __repr__(self):
        return "{} -> {}".format(self.__condition, self.__result)


def parse_rule(script: str) -> Rule:
    script = script.replace(" ", "")
    condition, result = script.split("->")
    condition = parse_logic(condition)

    return Rule(condition, result)


if __name__ == "__main__":
    print(parse_rule("a|!c -> b"))
