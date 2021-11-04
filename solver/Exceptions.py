class AxiomException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RuleConflictException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PatternException(Exception):
    def __init__(self, *args):
        super().__init__(*args)