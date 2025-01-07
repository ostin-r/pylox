from lox_token import Token, TokenType

class Scanner:
    def __init__(self, source: str, interpreter):
        self.source = source
        self.interpreter = interpreter
        self.tokens = []
        self.start = 0  # track the start of the current lexeme, not to be confused with start of the file
        self.current = 0
        self.line = 1

        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }

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

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def match_next(self, expected_char: str) -> bool:
        if self.is_end_of_file():
            return False
        if self.source[self.current] != expected_char:
            return False
        self.current += 1
        return True

    def is_end_of_file(self):
        return self.current >= len(self.source)

    def add_token(self, token_type: TokenType, literal: str | None = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
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
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    self.interpreter.pylox_error(self.line, f'unexpected character: {c}')


    def is_digit(self, c):
        return c >= '0' and c <= '9'


    def string(self):
        while (self.peek() != '"' and not self.is_end_of_file()):
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if (self.is_end_of_file()):
            self.interpreter.pylox_error(self.line, 'Unterminated string')
            return None

        self.advance()
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)


    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))


    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def is_alpha(self, c: str):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def is_alphanumeric(self, c: str):
        return self.is_alpha(c) or self.is_digit(c)
    
