class AxiomException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RuleConflictException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PatternException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class SolverConflictException(Exception):
    def __init__(self, msg: str, trace: list, entity: set):
        super().__init__(msg + "; start: {}; rule trace: ".format(entity) + str(trace))