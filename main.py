import sys
from scanner import Scanner

class LoxInterpreter:
    def __init__(self):
        self.had_error = False

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

        # for now just print the tokens
        for token in tokens:
            print(token)

    def pylox_error(self, line_no: int, message: str) -> None:
        self.had_error = True
        print("[line " + str(line_no) + "] Error: " + message)

    def main(self):
        if len(sys.argv) > 2:
            print("Incorrect amount of arguments, usage: python3 main.py <lox script>")
            sys.exit()
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

def main():
    interpreter = LoxInterpreter()
    interpreter.main()

if __name__ == "__main__":
    main()

