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

    def convert_ndfa_to_dfa(self):
        dfa_states = {}
        queue = []
        start_state = frozenset([self.q0])

        dfa_states[start_state] = "q0"
        queue.append(start_state)
        dfa_transitions = {}

        while queue:
            current_set = queue.pop(0)
            dfa_state_name = dfa_states[current_set]

            for symbol in self.sigma:
                new_set = set()
                for state in current_set:
                    if state in self.delta and symbol in self.delta[state]:
                        new_set.update(self.delta[state][symbol])

                if new_set:
                    frozen_new_set = frozenset(new_set)
                    if frozen_new_set not in dfa_states:
                        dfa_states[frozen_new_set] = f"q{len(dfa_states)}"
                        queue.append(frozen_new_set)

                    dfa_transitions[dfa_state_name, symbol] = dfa_states[frozen_new_set]

        return dfa_transitions, dfa_states


