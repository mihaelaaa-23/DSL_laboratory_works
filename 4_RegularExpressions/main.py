from generator import Generator

expressions = [
    "(S|T)(U|V)W*Y+24",
    "L(M|N)O{3}P*Q(2|3)",
    "R*S(T|U|V)W(X|Y|Z){2}"
]

for expr in expressions:
        print(f"\nGenerated strings for expression: {expr}")
        generator = Generator(expr)
        generator.generate_n_strings()