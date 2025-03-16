from lox_callable import LoxCallable
from lox_instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict):
        assert isinstance(name, str)
        assert isinstance(methods, dict)

        self.name = name
        self.methods = methods

    def find_method(self, method_name: str):
        if method_name in self.methods:
            return self.methods[method_name]
        return None

    def call(self, interpreter, arguments):
        lox_instance = LoxInstance(self)
        return lox_instance

    def arity(self):
        return 0
        
    def __str__(self):
        return f'<Lox Class:{self.name}>'
    
