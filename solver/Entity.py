class Entity:
    def __init__(self, attrs: set):
        self.__attrs = attrs

    def has_attr(self, attr) -> bool:
        return attr in self.__attrs

    def add_attr(self, attr):
        attr.replace(" ", "")

        if "&" in attr:
            for at in attr.split("&"):
                self.add_attr(at)

        if attr[0] == "!":
            self.__del_attr(attr[1:])
        else:
            self.__attrs.add(attr)

    def __del_attr(self, attr):
        self.__attrs.discard(attr)

    @property
    def attrs(self):
        return self.__attrs.copy()

    def __repr__(self):
        return "{}".format(self.__attrs)