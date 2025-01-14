from expr import Expr
from lox_token import TokenType
from runtime_error import LoxRuntimeError
from stmt import PrintStatement, ExpressionStatement, VarStatement, Stmt
from typing import List
from environment import Environment

class Interpreter:

    def __init__(self, main):
        self.main = main
        self.environment = Environment()
    
    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            self.main.runtime_error(e)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def visit_expression_statement(self, stmt: ExpressionStatement):
        self.evaluate(stmt.expression)
        return None

    def visit_print_statement(self, stmt: PrintStatement):
        value = self.evaluate(stmt.expression)
        print(value)
        return None

    def visit_var_statement(self, stmt: VarStatement):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_literal_expr(self, expr: Expr):
        return expr.value

    def visit_grouping_expr(self, expr: Expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Expr):
        right = self.evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not right

    def visit_var_expr(self, expr: Expr):
        return self.environment.get(expr.name)

    def visit_binary_expr(self, expr: Expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                # number check must be used on each individual case because addition is overridden by strings
                self.check_number_operand_binary(expr.operator, left, right)
                return left - right
            case TokenType.SLASH:
                self.check_number_operand_binary(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.check_number_operand_binary(expr.operator, left, right)
                return left * right
            case TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                raise LoxRuntimeError(expr.operator, "Operands must be matching strings or numbers")

    def is_truthy(self, value):
        """
            Lox considers false and nil as falsey
            Everything else is truthy
        """
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        else:
            return True

    def is_equal(self, a, b):
        """
            A simple function for now. Custom behavior for objects, etc. may be added here later
        """
        return a == b

    def check_number_operand(self, operator, operand):
        if not isinstance(operand, float):
            raise LoxRuntimeError(operator, 'Operand must be a number')

    def check_number_operand_binary(self, operator, left, right):
        if not isinstance(left, float) or not isinstance(right, (float, int)):
            raise LoxRuntimeError(operator, 'Operands must be numbers')

    def stringify(self, value):
        if value is None:
            return 'nil'
        if isinstance(value, float):
            text = str(value)
            if text.endswith('.0'):
                text = text[:-2]
            return text
        return str(value)

           
