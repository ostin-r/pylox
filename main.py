import sys

def run_file(file_name):
    with open(file_name) as f:
        read_data = f.read()
    run(read_data)

def run_prompt():
    while True:
        user_input = input("> ")
        if not len(user_input):
            break
        run(user_input)

def run():
    scanner = Scanner()
    tokens = scanner.scan_tokens()

    # for now just print the tokens
    for token in tokens:
        print(token)

def main():
    if len(sys.argv) > 2:
        print("Usage: jlox <script>")
        sys.exit()
    else if len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

if __name__ == "__main__":
    main()

