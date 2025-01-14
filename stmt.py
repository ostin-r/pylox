from expr import Expr
from lox_token import Token

class Stmt:
	def accept(self, visitor):
		pass

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
		assert isinstance(initializer, (Expr, None))

		self.name = name
		self.initializer = initializer

	def accept(self, visitor):
		return visitor.visit_var_statement(self)
