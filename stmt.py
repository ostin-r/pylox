from expr import Expr

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

