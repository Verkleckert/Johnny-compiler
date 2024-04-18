from parser_ import *
from generator_ import *

johnny_path = "I:\johnny\\"

def print_ast(node, level=0):
    """
    Recursively prints the Abstract Syntax Tree (AST).

    Args:
    - node: Root node of the AST.
    - level: Current depth of the node in the tree.
    """
    if node:
        print("  " * level + str(node.type) + ((": " + str(node.value)) if node.value is not None else ""))
        for child in node.children:
            print_ast(child, level + 1)

if __name__ == "__main__":
    # expression = input("Enter a mathematical expression: ")
    # expression = "(1/(2+3))*(4/(5+6))"
    expression = "234-100+50-10"
    tokens = tokenize_expression(expression)
    ast_root = parse_tokens(tokens)
    print("Abstract Syntax Tree (AST):")
    print_ast(ast_root)

    instructions = generate_assembly(ast_root)
    # ram.insert(0, generate_data(5, entry_point))
    print("Assembly Instructions:")
    print(instructions)
    
    with open(johnny_path + "parserout.ram", "w") as f:
        for i in range(1000):
            if instructions.get(i):
                f.write(str(instructions.get(i)) + "\n")
            else:
                f.write("000\n")