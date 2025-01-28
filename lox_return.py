from runtime_error import LoxRuntimeError

class Return(LoxRuntimeError):

    def __init__(self, value):
        super().__init__(value, '')
        self.value = value

