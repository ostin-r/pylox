from typing import List
from token import Token, TokenType
from main import LoxInterpreter

class Scanner:
    def __init__(self, source: str, interpreter: LoxInterpreter):
        self.source = source
        self.interpreter = interpreter
        self.tokens = []
        self.start = 0  # track the start of the current lexeme, not to be confused with start of the file
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while self.current < len(self.source):
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        self.current += 1
        c = self.source[self.current]
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case _:
                self.interpreter.pylox_error(self.line, 'unexpected character')

    def add_token(self, token_type: TokenType, literal: dict | None = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

