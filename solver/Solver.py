from solver.Rules import Rule, parse_rule
from solver.Logic import *
from solver.Entity import Entity


class Solver:
    def __init__(self):
        self.__rules: set[Rule] = set()

    def add_rule(self, rule: [Rule, str]):
        rule = rule if isinstance(rule, Rule) else parse_rule(rule)
        self.__rules.add(rule)
        self.__rebuild_rules(rule.result)

    def solve(self, entity: [Entity, set]) -> Entity:
        entity = entity if isinstance(entity, Entity) else Entity(entity)

        cached = entity.attrs
        while True:
            for rule in self.__rules:
                rule.product(entity)
            if cached == entity.attrs:
                break
            else:
                cached = entity.attrs
        return entity

    @property
    def rules(self):
        return self.__rules

    def __rebuild_rules(self, result):
        matched_rules = set(filter(lambda x: x.result == result, self.__rules))
        if len(matched_rules) > 1:
            new_rule = Rule(Or(*[r.condition for r in matched_rules]), result)

            self.__rules.difference_update(matched_rules)
            self.__rules.add(new_rule)

    def __repr__(self):
        result = ""
        for rule in self.__rules:
            result += "{}\n".format(rule)
        return result


if __name__ == "__main__":
    s1 = Solver()

    s1.add_rule(Rule(1, 2))
    s1.add_rule(Rule(Or(2, 3), 4))
    s1.add_rule(Rule(5, 4))
    s1.add_rule(Rule(4, 5))

    print(s1)

    e = Entity({1})
    s1.solve(e)

    print(e.attrs)
