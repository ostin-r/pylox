from lox_token import Token


class Expr:
	pass


class VarExpr(Expr):
	def __init__(self, name: Token):
		assert isinstance(name, Token)
		self.name = name

	def accept(self, visitor):
		return visitor.visit_var_expr(self)


class AssignExpr(Expr):
	def __init__(self, name: Token, value: Expr):
		assert isinstance(name, Token)
		assert isinstance(value, Expr)
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visit_assign_expr(self)


class Binary(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		assert isinstance(left, Expr)
		assert isinstance(operator, Token)
		assert isinstance(right, Expr)

		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visit_binary_expr(self)


class Grouping(Expr):
	def __init__(self, expression: Expr):
		assert isinstance(expression, Expr)

		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_grouping_expr(self)


class Literal(Expr):
	def __init__(self, value: object):
		assert isinstance(value, object)

		self.value = value

	def accept(self, visitor):
		return visitor.visit_literal_expr(self)


class Unary(Expr):
	def __init__(self, operator: Token, right: Expr):
		assert isinstance(operator, Token)
		assert isinstance(right, Expr)

		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visit_unary_expr(self)

