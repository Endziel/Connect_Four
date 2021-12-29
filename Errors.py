
class LogicErrors(Exception):
    pass

class FullColumnException(LogicErrors):
    """
    blad przy wrzucaniu monety do pelnej kolumny
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)