
class Scanner:
    def __init__(self, source: str, tokens: List[Token]):
        self.source = source
        self.tokens = tokens
        self.start = 0  # track the start of the current lexeme, not to be confused with start of the file
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while self.current < len(self.source):
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, line))
        return self.tokens

    def scan_token():
        self.current += 1
        c = self.source[self.current]
        match c:
            case '(': add_token(TokenType.LEFT_PAREN)
            case ')': add_token(TokenType.RIGHT_PAREN)
            case '{': add_token(TokenType.LEFT_BRACE)
            case '}': add_token(TokenType.RIGHT_BRACE)
            case ',': add_token(TokenType.COMMA)
            case '.': add_token(TokenType.DOT)
            case '-': add_token(TokenType.MINUS)
            case '+': add_token(TokenType.PLUS)
            case ';': add_token(TokenType.SEMICOLON)
            case '*': add_token(TokenType.STAR)
            case _:
                Lox.pylox_error(line, 'unexpected character")

    def add_token(token_type: TokenType, literal: dict or None = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, line))

