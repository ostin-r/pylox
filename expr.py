from lox_token import Token

class Expr:
	pass

class Binary(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		assert isinstance(left, Expr)
		assert isinstance(operator, Token)
		assert isinstance(right, Expr)

		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		self.visit_binary_expr(self)

class Grouping(Expr):
	def __init__(self, expression: Expr):
		assert isinstance(expression, Expr)

		self.expression = expression

	def accept(self, visitor):
		self.visit_grouping_expr(self)

class Literal(Expr):
	def __init__(self, value: object):
		assert isinstance(value, object)

		self.value = value

	def accept(self, visitor):
		self.visit_literal_expr(self)

class Unary(Expr):
	def __init__(self, operator: Token, right: Expr):
		assert isinstance(operator, Token)
		assert isinstance(right, Expr)

		self.operator = operator
		self.right = right

	def accept(self, visitor):
		self.visit_unary_expr(self)

