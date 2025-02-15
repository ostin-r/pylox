import sys

# Generates <base_name>.py in the calling directory
# Meta programming to generate classes used by the interpreter
# This file is not actually used in the interpreter, it just outputs classes into a convenient file
# Used to create expr.py, stmt.py

class GenerateAST:
    def main(self):
        if len(sys.argv) != 1:
            print("Incorrect amount of arguments, usage: generate_ast.py in the working directory")
            sys.exit()
        print('Creating file...')
        type_descriptions = {
            'Expression': [['Expr', 'expression']],
            'Print': [['Expr', 'expression']]
        }
        self.define_ast("stmt", type_descriptions)

        
    def define_ast(self, base_name, type_descriptions):
        """ Writes classes to be used in the AST to expr.py """
        file = base_name + '.py'
        with open(file, 'x') as f:
            # f.write('from lox_token import Token\n\n')
            # f.write('class ExprVisitor:\n')
            # for class_name in type_descriptions.keys():
            #     f.write(f'\tdef visit_{class_name.lower()}_{base_name}(self):\n')
            #     f.write('\t\tpass\n\n')

            f.write(f'class {base_name.capitalize()}:\n')
            f.write('\t@abstractmethod\n')
            f.write('\tdef accept(self, visitor: ExprVisitor):\n')
            f.write('\t\tpass\n\n')

            for class_name, class_info in type_descriptions.items():
                print(f'writing class name = {class_name}')
                arguments = [f'{info[1]}: {info[0]}' for info in class_info]
                arg_string = ', '.join(arguments)
                f.write(f'class {class_name}({base_name.capitalize()}):\n')
                f.write(f'\tdef __init__(self, {arg_string}):\n')
                for argument_types in class_info:
                    f.write(f'\t\tassert isinstance({argument_types[1]}, {argument_types[0]})\n')
                f.write('\n')
                for argument_types in class_info:
                    f.write(f'\t\tself.{argument_types[1]} = {argument_types[1]}\n')
                f.write('\n')

                f.write('\tdef accept(self, visitor):\n')
                f.write(f'\t\treturn visitor.visit_{class_name.lower()}_{base_name}(self)\n')
                f.write('\n')

 
if __name__ == '__main__':
    gen_ast = GenerateAST()
    gen_ast.main()

