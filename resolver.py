from typing import List, Union
from enum import Enum, auto
from stmt import Stmt, BlockStatement, VarStatement, FunctionStatement, ExpressionStatement, IfStatement, PrintStatement, \
                 ReturnStatement, WhileStatement, ClassStatement
from expr import Expr, Binary, CallExpr, Grouping, Literal, LogicalExpr, Unary, GetExpr, SetExpr



class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver:
    def __init__(self, interpreter, lox):
        self.interpreter = interpreter
        self.lox = lox
        self.scopes = []
        self.current_function = FunctionType.NONE

    def visit_block_statement(self, stmt: BlockStatement):
        self.begin_scope()
        self.resolve_list(stmt.statements)
        self.end_scope()

    def visit_class_statement(self, stmt: ClassStatement):
        self.declare(stmt.name)
        self.define(stmt.name)

    def visit_var_statement(self, stmt: VarStatement):
        self.declare(stmt.name)
        if (stmt.initializer is not None):
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visit_var_expr(self, expr: Expr):
        if len(self.scopes) and self.scopes[-1].get(expr.name.lexeme) is False:
            self.interpreter.main.pylox_error(expr.name.line, 'Cannot read local variable in its own initializer')
        self.resolve_local(expr, expr.name)

    def visit_assign_expr(self, expr: Expr):
        self.resolve(expr.value)  # first resolve any variables in assignment
        self.resolve_local(expr, expr.name)

    def visit_function_statement(self, stmt: FunctionStatement):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_expression_statement(self, stmt: ExpressionStatement):
        self.resolve(stmt.expression)

    def visit_if_statement(self, stmt: IfStatement):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print_statement(self, stmt: PrintStatement):
        self.resolve(stmt.expression)

    def visit_return_statement(self, stmt: ReturnStatement):
        if self.current_function == FunctionType.NONE:
            self.lox.pylox_error(stmt.keyword.line, "Cannot return from top-level code")
        if stmt.value is not None:
            self.resolve(stmt.value)
        
    def visit_while_statement(self, stmt: WhileStatement):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_binary_expr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr: CallExpr):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visit_get_expr(self, expr: GetExpr):
        self.resolve(expr.object)

    def visit_grouping_expr(self, expr: Grouping):
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return None

    def visit_logical_expr(self, expr: LogicalExpr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_set_expr(self, expr: SetExpr):
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visit_unary_expr(self, expr: Unary):
        self.resolve(expr.right)

    def resolve_function(self, stmt: FunctionStatement, function_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for param in stmt.params:
            self.declare(param)
            self.define(param)
        self.resolve_list(stmt.body)
        self.end_scope()

        self.current_function = enclosing_function

    def resolve_local(self, expr, name):
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
        
    def resolve_list(self, statements: List[Stmt]):
        for statement in statements:
            self.resolve(statement)
        
    def resolve(self, statement: Union[Expr, Stmt]):
        statement.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if not len(self.scopes):
            return None
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.lox.pylox_error(name.line, "Already a variable with this name in scope")

        scope[name.lexeme] = False

    def define(self, name):
        if not len(self.scopes):
            return None
        scope = self.scopes[-1]
        scope[name.lexeme] = True

