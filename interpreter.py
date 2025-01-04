from expr import Expr
from token import TokenType

class Interpreter:
    def visit_literal_expr(self, expr: Expr):
        return expr.value

    def visit_grouping_expr(self, expr: Expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Expr):
        right = self.evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                return -right
            case TokenType.BANG:
                return not right

    def visit_binary_expr(self, expr: Expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                return left - right
            case TokenType.SLASH:
                return left / right
            case TokenType.STAR:
                return left * right
            case TokenType.PLUS:
                return left + right
            

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def is_truthy(self, value):
        """
            Lox considers false and nil as falsey
            Everything else is truthy
        """
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        else:
            return True

    def is_equal(self, a, b):
        """
            A simple function for now, custom behavior for objects, etc. may be added here later
        """
        return a == b
           
