from lox_callable import LoxCallable
from stmt import FunctionStatement
from environment import Environment
from lox_return import Return

class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStatement, closure: Environment, is_initializer: bool):
        assert isinstance(declaration, FunctionStatement)
        assert isinstance(closure, Environment)
        assert isinstance(is_initializer, bool)
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
        
    def call(self, interpreter, arguments: list):
        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            param = self.declaration.params[i]
            argument = arguments[i]
            environment.define(param.lexeme, argument)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, 'this')
            return return_value.value

        if self.is_initializer:
            return self.closure.get_at(0, 'this')  # force return of 'this' for class initializers
        return None

    def arity(self):
        return len(self.declaration.params)

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define('this', instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'

