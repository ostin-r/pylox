from enum import Enum

class TokenType(Enum):
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '['
    RIGHT_BRACE = ']'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<=' 
    IDENTIFIER = 'identifier'
    STRING = 'string'
    NUMBER = 'number'
    AND = 'and'
    CLASS = 'class' 
    ELSE = 'else' 
    FALSE = 'false'
    FUN = 'fun' 
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print' 
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'
    EOF = 'end_of_file'


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: dict | None, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return str(self.token_type) + " " + self.lexeme + " " + str(self.literal)


