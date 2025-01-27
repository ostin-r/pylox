from typing import List
from lox_token import Token, TokenType
from expr import Literal, Binary, Unary, Grouping, VarExpr, AssignExpr, LogicalExpr, CallExpr
from error_handling import ParseError
from stmt import PrintStatement, ExpressionStatement, VarStatement, BlockStatement, IfStatement, \
                 WhileStatement, FunctionStatement

# recursive decent pattern for parsing tokens


class Parser:

    MAX_FUNC_PARAMETERS = 255
    
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
            if self.match([TokenType.FUN]):
                return self.function_declaration('function')
            if self.match([TokenType.VAR]):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self):
        if self.match([TokenType.FOR]):
            return self.for_statement()
        if self.match([TokenType.IF]):
            return self.if_statement()
        if self.match([TokenType.PRINT]):
            return self.print_statement()
        if self.match([TokenType.WHILE]):
            return self.while_statement()
        if self.match([TokenType.LEFT_BRACE]):
            return BlockStatement(self.block())
        return self.expression_statement()

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after for")

        initializer = None
        if self.match([TokenType.SEMICOLON]):
            initializer = None
        elif self.match([TokenType.VAR]):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after for loop condition")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after for clause")
        body = self.statement()

        if increment is not None:
            body = BlockStatement([body, ExpressionStatement(increment)])
        if condition is None:
            condition = Literal(True)
        body = WhileStatement(condition, body)
        if initializer is not None:
            body = BlockStatement([initializer, body])
        
        return body


    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after if statement")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if statement")
        then_branch = self.statement()
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()
        return IfStatement(condition, then_branch, else_branch)

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

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after if statement")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if statement")
        body = self.statement()
        return WhileStatement(condition, body)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return ExpressionStatement(expr)

    def function_declaration(self, kind: str):
        name = self.consume(TokenType.IDENTIFIER, f'Expected {kind} name')

        self.consume(TokenType.LEFT_PAREN, f'Expected "(" after {kind} name')
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, 'Expected parameter name'))
            while self.match([TokenType.COMMA]):
                if len(parameters) > self.MAX_FUNC_PARAMETERS:
                    self.error(self.peek(), 'Parameter length exceeded: cannot have more than 255 parameters')
                parameters.append(self.consume(TokenType.IDENTIFIER, 'Expected parameter name'))
        self.consume(TokenType.RIGHT_PAREN, 'Expected ")" after parameters')

        self.consume(TokenType.LEFT_BRACE, f'Expected "{'{'}" before {kind} body')  # block() expects right brace to be parsed already
        body = self.block()
        return FunctionStatement(name, parameters, body)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_end_of_file():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.or_exp()
        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, VarExpr):
                name = expr.name
                return AssignExpr(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def or_exp(self):
        expr = self.and_exp()
        while self.match([TokenType.OR]):
            operator = self.previous()
            right = self.and_exp()
            expr = LogicalExpr(expr, operator, right)
        return expr

    def and_exp(self):
        expr = self.equality()
        while self.match([TokenType.AND]):
            operator = self.previous()
            right = self.equality()
            expr = LogicalExpr(expr, operator, right)
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
        return self.call()

    def call(self):
        expr = self.primary()
        while True:
            if self.match([TokenType.LEFT_PAREN]):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, callee):
        # handle arguments of a function call
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match([TokenType.COMMA]):
                if len(arguments) > self.MAX_FUNC_PARAMETERS:
                    self.error(callee, 'Maximum number of arguments provided to function: 255')
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, 'Expected ")" after function arguments.')
        return CallExpr(callee, paren, arguments)
            

    def primary(self):
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)
        if self.match([TokenType.NIL]):
            return Literal(None)
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
        print(token)
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
                
