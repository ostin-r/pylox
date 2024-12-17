from expr import Unary, Literal, Grouping, Binary
from lox_token import Token, TokenType


class ASTPrinter:
    def print(self, expr):
        print(expr.accept(self))

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator, [expr.left, expr.right])

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator, [expr.right])

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", [expr.expression])

    def visit_literal_expr(self, expr):
        return str(expr.value)

    def parenthesize(self, name, exprs):
        expr_str = f'({name} '
        for expr in exprs:
            expr_str += f'{expr.accept(self)}'
        expr_str += ')'
        return expr_str

if __name__ == '__main__':
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, '-', None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(Literal(45.67))
    )
    ast_printer = ASTPrinter()
    ast_printer.print(expression)