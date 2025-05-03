from tokenizer import tokenize
from parser import Parser

from ast_nodes import (
    BinaryOpNode,
    UnaryOpNode,
    NumberNode,
    VariableNode,
    AssignmentNode,
    FunctionCallNode,
    AbsoluteValueNode
)


def print_ast(node, indent=0):
    if node is None:
        return

    indent_str = '  ' * indent

    if isinstance(node, NumberNode):
        print(f"{indent_str}Number({node.value})")

    elif isinstance(node, AssignmentNode):
        print(f"{indent_str}Assignment")
        print(f"{indent_str}  Variable: {node.variable}")
        print(f"{indent_str}  Value: ", end='')
        print_ast_value(node.value)

    elif isinstance(node, BinaryOpNode):
        op_value = node.op.value if hasattr(node.op, 'value') else node.op
        print(f"{indent_str}BinaryOp({op_value}, ", end='')
        print_ast_value(node.left)
        print(", ", end='')
        print_ast_value(node.right)
        print(")")

    elif isinstance(node, UnaryOpNode):
        op_value = node.op.value if hasattr(node.op, 'value') else node.op
        print(f"{indent_str}UnaryOp({op_value}, ", end='')
        print_ast_value(node.expr)
        print(")")

    elif isinstance(node, FunctionCallNode):
        print(f"{indent_str}Function({node.name}, ", end='')
        print_ast_value(node.args)
        print(")")

    elif isinstance(node, AbsoluteValueNode):
        print(f"{indent_str}Abs(", end='')
        print_ast_value(node.expr)
        print(")")

    elif isinstance(node, VariableNode):
        print(f"{indent_str}Variable({node.name})")

    else:
        # Generic fallback
        print(f"{indent_str}{node}")


def print_ast_value(node):
    if node is None:
        print("None", end='')
        return

    if isinstance(node, NumberNode):
        print(f"Number({node.value})", end='')

    elif isinstance(node, BinaryOpNode):
        op_value = node.op.value if hasattr(node.op, 'value') else node.op
        print(f"BinaryOp({op_value}, ", end='')
        print_ast_value(node.left)
        print(", ", end='')
        print_ast_value(node.right)
        print(")", end='')

    elif isinstance(node, UnaryOpNode):
        op_value = node.op.value if hasattr(node.op, 'value') else node.op
        print(f"UnaryOp({op_value}, ", end='')
        print_ast_value(node.expr)
        print(")", end='')

    elif isinstance(node, FunctionCallNode):
        print(f"Function({node.name}, ", end='')
        print_ast_value(node.args)
        print(")", end='')

    elif isinstance(node, AbsoluteValueNode):
        print(f"Abs(", end='')
        print_ast_value(node.expr)
        print(")", end='')

    elif isinstance(node, VariableNode):
        print(f"Variable({node.name})", end='')

    else:
        print(f"{node}", end='')


def test_parser(expr, use_regex_lexer=False):
    print(f"Expression: {expr}")
    print(f"Using {'Regex-based' if use_regex_lexer else 'Character-based'} Lexer")

    tokens = tokenize(expr, use_regex=use_regex_lexer)
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")

    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAST Structure:")
    print_ast(ast)
    print("\n" + "-" * 50)


expressions = [
    "3.14",
    "x = 5 + 3",
    "y = 2 * (4 - 1)",
    "z = 10 / (2 + 3)",
    "a = 2^3",
    "b = -5",
    "c = |x - y|",
    "sin(30)",
    "5!",
    "7 % 3"
]

print("\nTESTING WITH CHARACTER-BASED LEXER")
print("*" * 50)

for expr in expressions:
    test_parser(expr, use_regex_lexer=False)
