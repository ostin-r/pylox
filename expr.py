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

class Grouping(Expr):
	def __init__(self, expression: Expr):
		assert isinstance(expression, Expr)

		self.expression = expression

class Literal(Expr):
	def __init__(self, value: str):
		assert isinstance(value, str)

		self.value = value

class Unary(Expr):
	def __init__(self, operator: Token, right: Expr):
		assert isinstance(operator, Token)
		assert isinstance(right, Expr)

		self.operator = operator
		self.right = right

