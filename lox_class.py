from lox_callable import LoxCallable
from lox_instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name: str):
        assert isinstance(name, str)
        self.name = name

    def call(self, interpreter, arguments):
        lox_instance = LoxInstance(self)
        return lox_instance

    def arity(self):
        return 0
        
    def __str__(self):
        return f'<Lox Class:{self.name}>'
    
