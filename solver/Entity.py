from solver.Exceptions import AxiomException


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
            if attr[0] == "!":
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
        return self.__false_attrs.copy() | self.__true_attrs.copy()

    def __repr__(self):
        return "{}".format(self.true_attrs | {"!{}".format(a) for a in self.false_attrs})


if __name__ == "__main__":
    e = Entity({"a", "b", "!c"})
    print(e.true_attrs)
    print(e.false_attrs)
    print(e.known_attrs)