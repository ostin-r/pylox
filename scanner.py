from typing import List
from lox_token import Token, TokenType
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
        while not self.is_end_of_file():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def advance(self):
        next = self.source[self.current]
        self.current += 1
        return next

    def peek(self):
        if self.is_end_of_file():
            return '\0'
        return self.source[self.current]

    def match_next(self, expected_char: str) -> bool:
        if self.is_end_of_file():
            return False
        if self.source[self.current] != expected_char:
            return False
        self.current += 1
        return True

    def is_end_of_file(self):
        return self.current >= len(self.source)

    def add_token(self, token_type: TokenType, literal: dict | None = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
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
            case '!':
                if self.match_next('='):
                    token_type = TokenType.BANG_EQUAL
                else:
                    token_type = TokenType.BANG
                self.add_token(token_type)
            case '=':
                if self.match_next('='):
                    token_type = TokenType.EQUAL_EQUAL
                else:
                    token_type = TokenType.EQUAL
                self.add_token(token_type)
            case '<':
                if self.match_next('='):
                    token_type = TokenType.LESS_EQUAL
                else:
                    token_type = TokenType.LESS
                self.add_token(token_type)
            case '>':
                if self.match_next('='):
                    token_type = TokenType.GREATER_EQUAL
                else:
                    token_type = TokenType.GREATER
                self.add_token(token_type)
            case '/':
                if self.match_next('/'):
                    while self.peek() != '\n':
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ':
                pass  # we do not care about whitespace in this house
            case '\r':
                pass  # we do not care about whitespace in this house
            case '\t':
                pass  # we do not care about whitespace in this house
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                self.interpreter.pylox_error(self.line, 'unexpected character')


    def string(self):
        pass

