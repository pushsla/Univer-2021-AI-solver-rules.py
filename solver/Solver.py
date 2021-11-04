from solver.Rules import Rule, parse_rule
from solver.Logic import *
from solver.Entity import Entity
from solver.Exceptions import *


class Solver:
    def __init__(self):
        self.__rules: set[Rule] = set()
        self.__rulechain: list[Rule] = list()  # BE CAREFUL! Do not use self.__rulechain.__contains__()

    def add_rule(self, rule: [Rule, str]):
        rule = rule if isinstance(rule, Rule) else parse_rule(rule)
        self.__rules |= rule.simplify()
        self.__rebuild_rules(rule.result)
        self.__rebuild_rulechain()

    def solve(self, entity: [Entity, set]) -> Entity:
        entity = entity if isinstance(entity, Entity) else Entity(entity)
        entity_for_trace = entity.known_attrs
        solve_trace = []

        cached = entity.known_attrs
        try:
            while True:
                for rule in self.__rulechain:
                    if rule.product(entity):
                        solve_trace.append(rule.__repr__())
                if cached == entity.known_attrs:
                    break
                else:
                    cached = entity.known_attrs
        except RuleConflictException as e:
            solve_trace.append(rule)
            raise SolverConflictException(' '.join(e.args), solve_trace, entity_for_trace)
        return entity

    @property
    def rules(self):
        return self.__rules.copy()

    @property
    def rulechain(self):
        return self.__rulechain.copy()

    def __rebuild_rules(self, result):
        matched_rules = set(filter(lambda x: x.result == result, self.__rules))
        if len(matched_rules) > 1:
            new_rule = Rule(Or(*[r.condition for r in matched_rules]), result)

            self.__rules.difference_update(matched_rules)
            self.__rules.add(new_rule)

    def __rebuild_rulechain(self):
        self.__rulechain = []

        for rule in self.__rules:
            index = len(self.__rulechain)+1
            for i, subrule in enumerate(self.__rulechain):
                if subrule.result.startswith(rule.result):
                    index = i
                    break
                elif subrule.result in rule.condition.used_axioms:
                    index = i
            self.__rulechain.insert(index, rule)

    def __repr__(self):
        result = ""
        for rule in self.__rules:
            result += "{}\n".format(rule)
        return result


if __name__ == "__main__":
    s1 = Solver()

    s1.add_rule(Rule(Or("b", "c"), "d"))
    s1.add_rule("b.pattern -> b.pattern.subpattern.subsubpattern")
    s1.add_rule(Rule("e", "d"))
    s1.add_rule(Rule("d", "c"))
    s1.add_rule("b.pattern -> b.pattern.subpattern")
    s1.add_rule("d -> b.pattern")
    s1.add_rule("d -> !b.pattern")
    s1.add_rule("b.pattern -> !b.false_pattern")
    s1.add_rule(Rule("a", "b"))

    print(s1)
    print(s1._Solver__rulechain)

    e = Entity({"a"})
    s1.solve(e)

    print(e.true_attrs)
    print(e.false_attrs)
    print(e)
