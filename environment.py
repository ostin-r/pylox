from lox_token import Token
from runtime_error import LoxRuntimeError

class Environment:
    """ Tracks variables """

    def __init__(self, enclosing: 'Environment' or None = None):
        # signature uses forward refrences to indicate that the enclosing arg is an Environment class type
        self.values = {}
        self.enclosing = enclosing

    def define(self, key, value):
        # note that since we overwrite without checking existence, the variable can be reassigned
        # via the "var" keyword
        self.values[key] = value

    def assign(self, name: Token, value):
        key = name.lexeme
        if key in self.values:
            self.values[key] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f'Undefined variable: {key}')

    def get(self, name: Token):
        key = name.lexeme
        if key in self.values:
            return self.values[key]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise LoxRuntimeError(name, f'Undefined variable: {key}')

