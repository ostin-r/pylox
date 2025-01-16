from typing import List
from lox_token import Token, TokenType
from expr import Literal, Binary, Unary, Grouping, VarExpr, AssignExpr
from error_handling import ParseError
from stmt import PrintStatement, ExpressionStatement, VarStatement, BlockStatement

# recursive decent pattern for parsing tokens
# 
# order of precedence, lowest to highest:
# equality (lowest)
# comparison
# addition
# multiplication
# unary
# literal (highest)

class Parser:
    def __init__(self, tokens: List[Token], interpreter):
        assert isinstance(tokens, list)
        self.tokens = tokens
        self.current = 0
        self.interpreter = interpreter

    def parse(self):
        statements = []
        while not self.is_end_of_file():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        try:
            if self.match([TokenType.VAR]):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self):
        if self.match([TokenType.PRINT]):
            return self.print_statement()
        if self.match([TokenType.LEFT_BRACE]):
            return BlockStatement(self.block())
        return self.expression_statement()

    def print_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after print statement.")
        return PrintStatement(expr)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        initializer = None
        if self.match([TokenType.EQUAL]):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VarStatement(name, initializer)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return ExpressionStatement(expr)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, VarExpr):
                name = expr.name
                return AssignExpr(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def equality(self):
        expr = self.comparison()
        equality_terms = [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        while self.match(equality_terms):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        comparison_terms = [TokenType.LESS_EQUAL, TokenType.LESS, TokenType.GREATER, TokenType.GREATER_EQUAL]
        while self.match(comparison_terms):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
            
    def term(self):
        # addition and subtraction
        expr = self.factor()
        terms = [TokenType.PLUS, TokenType.MINUS]
        while self.match(terms):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        # multiplication and division
        expr = self.unary()
        factor_terms = [TokenType.STAR, TokenType.SLASH]
        while self.match(factor_terms):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        unary_terms = [TokenType.BANG, TokenType.MINUS]
        if self.match(unary_terms):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)
        if self.match([TokenType.STRING, TokenType.NUMBER]):
            return Literal(self.previous().literal)
        if self.match([TokenType.IDENTIFIER]):
            return VarExpr(self.previous())
        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'Expect ")" after expression')
            return Grouping(expr)
        raise self.error(self.peek(), 'Expected expression')

    def match(self, token_types: list) -> bool:
        if self.peek().token_type in token_types:
            self.advance()
            return True
        return False

    def consume(self, expected_token_type, error_message):
        if self.peek().token_type == expected_token_type:
            return self.advance()
        error_message += f" Got {self.peek().token_type} instead."
        raise self.error(self.peek(), error_message)
        
    def check(self, check_type):
        if self.is_end_of_file():
            return False
        return self.peek().token_type == check_type

    def advance(self):
        if not self.is_end_of_file():
            self.current += 1
        return self.previous()

    def is_end_of_file(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, error_message):
        self.interpreter.pylox_error(token.line, error_message)
        # Return object instead of raising to allow calling method to decide what to do with it
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.is_end_of_file():
            if self.previous().token_type == TokenType.SEMICOLON:
                return None
            match self.peek().token_type:
                case TokenType.CLASS:
                    pass
                case TokenType.FUN:
                    pass
                case TokenType.VAR:
                    pass
                case TokenType.FOR:
                    pass
                case TokenType.VAR:
                    pass
                case TokenType.IF:
                    pass
                case TokenType.WHILE:
                    pass
                case TokenType.PRINT:
                    pass
                case TokenType.RETURN:
                    return None
            self.advance()
                
