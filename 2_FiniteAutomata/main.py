from grammar import Grammar
from finite_automaton import FiniteAutomaton

grammar = Grammar()

fa = grammar.to_finite_automaton()

grammar_type = grammar.classify_chomsky()
print("\nGrammar Classification for Lab1:", grammar_type)

# Variant 28
q = {"q0", "q1", "q2", "q3"}
sigma = {"a", "b", "c"}
delta = {
    "q0": {"a": {"q0", "q1"}, "b": {"q2"}},
    "q1": {"a": {"q1"}, "b": {"q3"}, "c": {"q2"}},
    "q2": {"b": {"q3"}},
}
q0 = "q0"
f = {"q3"}

fa = FiniteAutomaton(q, sigma, delta, q0, f)

is_dfa = fa.is_deterministic()
print("\nThe FA is", "Deterministic (DFA)" if is_dfa else "Non-Deterministic (NFA)")

#convert NDFA to DFA if necessary
if not is_dfa:
    dfa_transitions, dfa_states = fa.convert_ndfa_to_dfa()
    print("\nDFA States:")
    for state, name in dfa_states.items():
        print(f"{name}: {set(state)}")

    print("\nDFA Transitions:")
    for (state, symbol), next_state in dfa_transitions.items():
        print(f"δ({state}, {symbol}) -> {next_state}")

grammar = Grammar()
fa_to_grammar = grammar.finite_automaton_to_grammar(fa)
print("\nFinite Automaton to Regular Grammar:")
for state, rules in fa_to_grammar.items():
    print(f"{state} -> {', '.join(rules)}")

fa.draw_automaton("automaton_28")


