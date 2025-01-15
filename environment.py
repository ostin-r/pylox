from lox_token import Token
from runtime_error import LoxRuntimeError

class Environment:
    """ Tracks variables """

    def __init__(self):
        self.values = {}

    def define(self, key, value):
        # note that since we overwrite without checking existence, the variable can be reassigned
        self.values[key] = value

    def assign(self, name: Token, value):
        key = name.lexeme
        if key in self.values:
            self.values[key] = value
        else:
            raise LoxRuntimeError(name, f'Undefined variable: {key}')

    def get(self, name: Token):
        key = name.lexeme
        if key in self.values:
            return self.values[key]
        raise LoxRuntimeError(name, f'Undefined variable: {key}')

