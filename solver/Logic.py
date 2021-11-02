from typing import Callable

from solver.Entity import Entity


class Logic:
    def __init__(self, *conditions):
        self.__conditions = conditions
        self.name = "Logic"

    def __make_production(self, conditions, entity: Entity) -> bool:
        raise NotImplementedError()

    def set_production(self, function: Callable):
        self.__make_production = function

    def product(self, entity: Entity) -> bool:
        return self.__make_production(self.__conditions, entity)

    def __repr__(self):
        return "{}{}".format(self.name, self.__conditions)


def logical(function):
    def wrapper(*conditions):
        lg = Logic(*conditions)
        lg.set_production(function)
        lg.name = function.__name__
        return lg

    return wrapper


@logical
def And(conditions, entity: Entity) -> bool:
    result = True
    for cond in conditions:
        if not result:
            break
        elif isinstance(cond, Logic):
            result = cond.product(entity)
        else:
            result = entity.has_attr(cond)
    return result

Is = And

@logical
def Or(conditions, entity: Entity) -> bool:
    result = False
    for cond in conditions:
        if result:
            break
        elif isinstance(cond, Logic):
            result = cond.product(entity)
        else:
            result = entity.has_attr(cond)
    return result


@logical
def Not(conditions, entity: Entity) -> bool:
    result = True
    for cond in conditions:
        if not result:
            break
        elif isinstance(cond, Logic):
            result = not cond.product(entity)
        else:
            result = not entity.has_attr(cond)
    return result


def parse_logic(script: str) -> Logic:
    script = script.replace(" ", "")
    cond = Logic
    scripts = []
    if "&" in script:
        scripts = script.split("&")
        cond = And
    elif "|" in script:
        scripts = script.split("|")
        cond = Or
    elif script[0] == "!":
        return Not(script[1:])
    else:
        return Is(script)

    return cond(*[parse_logic(sc) for sc in scripts])


if __name__ == "__main__":
    print(parse_logic("a&!b|c"))
