from solver.Logic import Logic, Is, parse_logic
from solver.Entity import Entity


class Rule:
    def __init__(self, condition, result):
        self.__condition = condition
        if not isinstance(condition, Logic):
            self.__condition = Is(condition)

        self.__result = result

    @property
    def result(self):
        return self.__result

    @property
    def condition(self):
        return self.__condition

    def product(self, entity: Entity):
        if self.__condition.product(entity):
            entity.add_attr(self.__result)

    def __repr__(self):
        return "{} -> {}".format(self.__condition, self.__result)


def parse_rule(script: str) -> Rule:
    script = script.replace(" ", "")
    condition, result = script.split("->")
    condition = parse_logic(condition)

    return Rule(condition, result)


if __name__ == "__main__":
    print(parse_rule("a|!c -> b"))
