from expr import Expr, VarExpr
from lox_token import Token
from typing import List

class Stmt:
	def accept(self, visitor):
		raise Exception('accept() method not yet implemented')

class FunctionStatement(Stmt):
	def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
		assert isinstance(name, Token)
		assert isinstance(params, list)
		assert isinstance(body, list)

		self.name = name
		self.params = params
		self.body = body

	def accept(self, visitor):
		return visitor.visit_function_statement(self)


class ClassStatement(Stmt):
	# def __init__(self, name: Token, super_class: VarExpr, methods: List[FunctionStatement]):
	def __init__(self, name: Token, methods: List[FunctionStatement]):
		assert isinstance(name, Token)
		# assert isinstance(super_class, VarExpr)
		assert isinstance(methods[0], FunctionStatement)

		self.name = name
		# self.super_class = super_class
		self.methods = methods

	def accept(self, visitor):
		return visitor.visit_class_statement(self)


class ReturnStatement(Stmt):
	def __init__(self, keyword: Token, value: Expr or None):
		assert isinstance(keyword, Token)
		if value is not None:
			assert isinstance(value, Expr)

		self.keyword = keyword
		self.value = value

	def accept(self, visitor):
		return visitor.visit_return_statement(self)


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

