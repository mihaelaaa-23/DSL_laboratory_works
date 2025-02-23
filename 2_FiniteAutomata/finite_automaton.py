from graphviz import Digraph

class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.f = f

    def string_belongs_to_language(self, input_string):
        current_state = self.q0

        for c in input_string:
            if c not in self.sigma or current_state not in self.delta:
                return False

            next_state = None
            if c in self.delta[current_state]:
                next_state = list(self.delta[current_state][c])[0]

            if next_state is None:
                return False

            current_state = next_state

        return current_state in self.f

    def is_deterministic(self):
        for state, transitions in self.delta.items():
            seen_symbols = set()
            for symbol in transitions:
                if symbol in seen_symbols:
                    return False  # Multiple transitions for the same input -> NDFA
                seen_symbols.add(symbol)
        return True


