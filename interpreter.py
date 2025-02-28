import time
from expr import Expr, AssignExpr, LogicalExpr
from lox_token import TokenType, Token
from runtime_error import LoxRuntimeError
from stmt import PrintStatement, ExpressionStatement, VarStatement, Stmt, BlockStatement, IfStatement, \
    WhileStatement, FunctionStatement, ReturnStatement
from typing import List
from environment import Environment
from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_return import Return


class Interpreter:

    def __init__(self, main):
        self.main = main
        self.globals = Environment()     # maintains a reference to outer most scope
        self.environment = self.globals  # changes as the interpreter enters blocks
        self.locals = {}                 # holds depth of resolved variables

        class Clock(LoxCallable):
            def arity(self):
                return 0

            def call(self, interpreter, arguments):
                return time.time()

            def __str__(self):
                return "<native fn 'clock'>"

        self.globals.define('clock', Clock())
    
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

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth
                             
    def visit_block_statement(self, stmt: BlockStatement):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_statement(self, stmt: ExpressionStatement):
        self.evaluate(stmt.expression)
        return None

    def visit_function_statement(self, stmt: FunctionStatement):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
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

    def visit_return_statement(self, stmt: ReturnStatement):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)

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
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
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
        return self.lookup_variable(expr.name, expr)

    def lookup_variable(self, name: Token, expr: Expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name)
        else:
            return self.globals.get(name)
            
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
                raise LoxRuntimeError(expr.operator, f"Operands must be matching strings or numbers, left={left} {type(left)}, right={right} {type(right)}")
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

    def visit_call_expr(self, expr: Expr):
        callee = self.evaluate(expr.callee)
        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(callee, 'Can only call functions and classes')
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if len(arguments) != callee.arity():
            raise LoxRuntimeError(expr.paren, f'Expected {callee.arity()} arguments but got {len(arguments)}')
        
        return callee.call(self, arguments)

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

           
