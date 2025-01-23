from expr import Expr
from lox_token import Token
from typing import List

class Stmt:
	def accept(self, visitor):
		pass

class WhileStatement(Stmt):
	def __init__(self, condition: Expr, body: Stmt):
		assert isinstance(condition, Expr)
		assert isinstance(body, Stmt)

		self.condition = condition
		self.body = body

	def accept(self, visitor):
		return visitor.visit_while_statement(self)

class ExpressionStatement(Stmt):
	def __init__(self, expression: Expr):
		assert isinstance(expression, Expr)

		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_expression_statement(self)

class PrintStatement(Stmt):
	def __init__(self, expression: Expr):
		assert isinstance(expression, Expr)

		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_print_statement(self)

class VarStatement(Stmt):
	def __init__(self, name: Token, initializer: Expr):
		assert isinstance(name, Token)
		if initializer is not None:
			assert isinstance(initializer, Expr)

		self.name = name
		self.initializer = initializer

	def accept(self, visitor):
		return visitor.visit_var_statement(self)

class BlockStatement(Stmt):
	def __init__(self, statements: List[Stmt]):
		assert isinstance(statements, list)

		self.statements = statements

	def accept(self, visitor):
		return visitor.visit_block_statement(self)

class IfStatement(Stmt):
	def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
		assert isinstance(condition, Expr)
		assert isinstance(then_branch, Stmt)
		if else_branch is not None:
			assert isinstance(else_branch, Stmt)

		self.condition = condition
		self.then_branch = then_branch
		self.else_branch = else_branch

	def accept(self, visitor):
		return visitor.visit_if_statement(self)

