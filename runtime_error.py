from lox_token import Token

class LoxRuntimeError(Exception):
    def __init__(self, operator: Token, message: str):
        self.operator = operator
        self.message = message
        super().__init__(message)
    
