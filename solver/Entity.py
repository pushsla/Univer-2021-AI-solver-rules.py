from solver.Exceptions import *


class Entity:
    def __init__(self, attrs: set[str] = None):
        attrs = attrs if attrs else {}

        self.__true_attrs = set()
        self.__false_attrs = set()

        for attr in attrs:
            self.set_known(attr)

    def set_known(self, attr: str):
        attr = attr.replace(" ", "")
        if isinstance(attr, str):
            if (is_pattern := parse_pattern(attr))[0]:
                self.set_pattern(is_pattern[1], is_pattern[2])
            elif attr[0] == "!":
                self.set_false(attr[1:])
            else:
                self.set_true(attr)
        else:
            raise TypeError("Unspported initial condition type: {}".format(type(attr)))

    def set_true(self, attr: str):
        if attr in self.__false_attrs:
            raise AxiomException("May not set '{}' as true and false axioms at same time".format(attr))
        self.__true_attrs.add(attr)

    def set_false(self, attr: str):
        if attr in self.__true_attrs:
            raise AxiomException("May not set '{}' as true and false axioms at same time".format(attr))
        self.__false_attrs.add(attr)

    def set_pattern(self, pattern_base: str, pattern_value: str):
        pattern_axiom = pattern_base[0] != "!"
        pattern_base = pattern_base if pattern_axiom else pattern_base[1:]

        if not self.is_true(pattern_base):
            raise PatternException("May not set pattern '{}' for '{}' due to not being this true axiom".format(pattern_value, pattern_base))

        full_pattern = "{}.{}".format(pattern_base, pattern_value)
        if pattern_axiom:
            self.set_true(full_pattern)
        else:
            self.set_false(full_pattern)

    def is_true(self, attr: str) -> bool:
        return attr in self.__true_attrs

    def is_false(self, attr: str) -> bool:
        return attr in self.__false_attrs

    def is_known(self, attr: str) -> bool:
        return self.is_true(attr) or self.is_false(attr)

    def unset(self, attr: str):
        self.__true_attrs.discard(attr)
        self.__false_attrs.discard(attr)

    @property
    def true_attrs(self):
        return self.__true_attrs.copy()

    @property
    def false_attrs(self):
        return self.__false_attrs.copy()

    @property
    def known_attrs(self):
        return self.__true_attrs.copy() | {"!"+x for x in self.__false_attrs}

    def __repr__(self):
        return "{}".format(self.true_attrs | {"!{}".format(a) for a in self.false_attrs})


def parse_pattern(axiom: str) -> tuple[bool, str, str]:
    if "." in axiom:
        pattern_value, pattern_base = (aspl := axiom.split("."))[-1], ".".join(aspl[:-1])
    else:
        return False, "", ""

    return True, pattern_base, pattern_value


if __name__ == "__main__":
    e = Entity({"tail", "milk", "horns"})
    e.set_known("animal")
    e.set_known("animal.mammal")
    e.set_known("animal.mammal.hoofed")
    e.set_known("!animal.mammal.unhoofed")
    print(e.true_attrs)
    print(e.false_attrs)
    print(e.known_attrs)