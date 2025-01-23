from expr import Expr, AssignExpr, LogicalExpr
from lox_token import TokenType
from runtime_error import LoxRuntimeError
from stmt import PrintStatement, ExpressionStatement, VarStatement, Stmt, BlockStatement, IfStatement, \
    WhileStatement
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

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
                             
    def visit_block_statement(self, stmt: BlockStatement):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_statement(self, stmt: ExpressionStatement):
        self.evaluate(stmt.expression)
        return None

    def visit_if_statement(self, if_statement: IfStatement):
        if_condition = self.evaluate(if_statement.condition)
        if self.is_truthy(if_condition):
            self.execute(if_statement.then_branch)
        elif if_statement.else_branch is not None:
            self.execute(if_statement.else_branch)
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

    def visit_while_statement(self, stmt: WhileStatement):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_assign_expr(self, expr: AssignExpr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_literal_expr(self, expr: Expr):
        return expr.value

    def visit_logical_expr(self, expr: LogicalExpr):
        left = self.evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

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
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

    def is_truthy(self, value):
        """
            False and Nil are falsy
            Everything else is truthy
        """
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        else:
            return True

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
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

           
