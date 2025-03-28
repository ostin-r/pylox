from lox_token import Token
from typing import List


class Expr:
	pass

class ThisExpr(Expr):
	def __init__(self, keyword: Token):
		assert isinstance(keyword, Token)
		self.keyword = keyword

	def accept(self, visitor):
		return visitor.visit_this_expr(self)

	
class CallExpr(Expr):
	def __init__(self, callee: Expr, paren: Token, arguments: List[Expr] or None):
		assert isinstance(callee, Expr)
		assert isinstance(paren, Token)
		if arguments is not None:
			assert isinstance(arguments, list)

		self.callee = callee
		self.paren = paren
		self.arguments = arguments

	def accept(self, visitor):
		return visitor.visit_call_expr(self)


class GetExpr(Expr):
	def __init__(self, object: Expr, name: Token):
		assert isinstance(object, Expr)
		assert isinstance(name, Token)

		self.object = object
		self.name = name

	def accept(self, visitor):
		return visitor.visit_get_expr(self)


class SetExpr(Expr):
	def __init__(self, object: Expr, name: Token, value: Expr):
		assert isinstance(object, Expr)
		assert isinstance(name, Token)
		assert isinstance(value, Expr)

		self.object = object
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visit_set_expr(self)


class LogicalExpr(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		assert isinstance(left, Expr)
		assert isinstance(right, Expr)
		assert isinstance(operator, Token)

		self.left = left
		self.right = right
		self.operator = operator

	def accept(self, visitor):
		return visitor.visit_logical_expr(self)


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

