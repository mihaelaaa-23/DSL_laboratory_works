from grammar import Grammar

grammar = Grammar()

print("Generated Strings:")
for _ in range(5):
    print(grammar.generate_string())

fa = grammar.to_finite_automaton()

print("\nCheck if strings belong to L:")
test_strings = ["aabb", "abaabb", "babb", "ab", "abababababababaaaaabb"]
for s in test_strings:
    print(f"'{s}' - {fa.string_belongs_to_language(s)}")