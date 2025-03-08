from lexer import Lexer

print("Running Lexer Tests")
test_expressions = [
    "3.14",
    "x = exp(2) + sqrt(5)",
    "x = |5| + |cos(-30)|",
    "x = 5+3 * 2",
    "y = -4.5 / 2 + sin(30)",
    "z = cos(60) * tan(45) - 7!",
    "a = 2^3 % 4",
    "b = cot(90) + 15",
    "c = (5 + 2) * 3 / 7"
]

for expr in test_expressions:
    print(f"\nExpression: {expr}")
    lexer = Lexer(expr)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
