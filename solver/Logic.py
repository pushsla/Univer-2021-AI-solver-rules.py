from solver.Entity import Entity


class Producting:
    def product(self, entity: Entity) -> bool:
        raise NotImplementedError()


class Logic(Producting):
    def __init__(self, *conditions):
        self._conditions = conditions
        self.name = self.__class__.__name__

    def product(self, entity: Entity) -> bool:
        return self._product(entity)

    @property
    def conditions(self) -> set:
        return set(self._conditions)

    @property
    def used_axioms(self) -> set:
        result = set()
        for cond in self._conditions:
            if isinstance(cond, Logic):
                result.update(cond.used_axioms)
            else:
                result.add(cond)

        return result

    def _product(self, entity: Entity) -> bool:
        raise NotImplementedError()

    def __repr__(self):
        return "{}{}".format(self.name, self._conditions)


class And(Logic):
    def _product(self, entity: Entity) -> bool:
        result = True
        for cond in self._conditions:
            if not result:
                break
            elif isinstance(cond, Logic):
                result = cond.product(entity)
            else:
                result = entity.is_true(cond)
        return result


class Is(And):
    pass


class Or(Logic):
    def _product(self, entity: Entity) -> bool:
        result = False
        for cond in self._conditions:
            if result:
                break
            elif isinstance(cond, Logic):
                result = cond.product(entity)
            else:
                result = entity.is_true(cond)
        return result


class Not(Logic):
    def _product(self, entity: Entity) -> bool:
        result = True
        for cond in self._conditions:
            if not result:
                break
            elif isinstance(cond, Logic):
                result = not cond.product(entity)
            else:
                result = entity.is_false(cond)
        return result


class SoftNot(Logic):
    def _product(self, entity: Entity) -> bool:
        result = True
        for cond in self._conditions:
            if not result:
                break
            elif isinstance(cond, Logic):
                result = not cond.product(entity)
            else:
                result = entity.is_false(cond) or (not entity.is_known(cond))
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
    elif script[0] == "?":
        return SoftNot(script[1:])
    else:
        return Is(script)

    return cond(*[parse_logic(sc) for sc in scripts])


if __name__ == "__main__":
    print(l := parse_logic("a & !b|c & ?c"))
    print(l.used_axioms)
