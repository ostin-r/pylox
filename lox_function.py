from lox_callable import LoxCallable
from stmt import FunctionStatement
from environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStatement):
        assert isinstance(declaration, FunctionStatement)
        self.declaration = declaration
        
    def call(self, interpreter, arguments: list):
        environment = Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            param = self.declaration.params[i]
            argument = arguments[i]
            environment.define(param.lexeme, argument)

        interpreter.execute_block(self.declaration.body, environment)
        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'

