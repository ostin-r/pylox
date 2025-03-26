from runtime_error import LoxRuntimeError
from lox_token import Token

class LoxInstance:
    def __init__(self, lox_class):
        self.lox_class = lox_class
        self.fields = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method = self.lox_class.find_method(name.lexeme)
        if method:
            return method.bind(self)
        raise LoxRuntimeError(name, f'Undefined property: {name.lexeme}')

    def set(self, name: Token, value):
        self.fields[name.lexeme] = value

    def __repr__(self):
        return f'{self.lox_class} instance'

