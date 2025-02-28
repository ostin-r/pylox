import sys
from scanner import Scanner
from parser import Parser
# from ast_printer import ASTPrinter
from runtime_error import LoxRuntimeError
from interpreter import Interpreter
from resolver import Resolver

class Lox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter(self)

    def run_file(self, file_name):
        with open(file_name) as f:
            read_data = f.read()
        self.run(read_data)
        if self.had_error:
            sys.exit()

    def run_prompt(self):
        while True:
            user_input = input("> ")
            if not len(user_input):
                break
            self.run(user_input)

    def run(self, data: str) -> None:
        scanner = Scanner(data, self)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, self)
        statements = parser.parse()
        if self.had_error or self.had_runtime_error:
            return None

        resolver = Resolver(self.interpreter, self)
        resolver.resolve_list(statements)

        if self.had_error:
            return None # stop for resolution errors

        self.interpreter.interpret(statements)

    def pylox_error(self, line_no: int, message: str) -> None:
        self.had_error = True
        print("[line " + str(line_no) + "] Error: " + message)

    def runtime_error(self, error: LoxRuntimeError) -> None:
        self.had_runtime_error = True
        print(error.message + f'[line {error.operator.line}]')

    def main(self):
        if len(sys.argv) > 2:
            print("Incorrect amount of arguments, usage: python3 main.py <lox script>")
            sys.exit()
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

def main():
    interpreter = Lox()
    interpreter.main()

if __name__ == "__main__":
    main()

