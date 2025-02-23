import random
from finite_automaton import FiniteAutomaton

class Grammar:
    def __init__(self):
        self.vn = {'S', 'A', 'B', 'C'}
        self.vt = {'a', 'b'}
        self.p = {
            'S': ['aA'],
            'A': ['bS', 'aB'],
            'B': ['bC', 'aB'],
            'C': ['aA', 'b']
        }
        self.start_symbol = 'S'

    def generate_string(self):
        string = self.start_symbol
        while any(v in string for v in self.vn):
            for v in string:
                if v in self.vn:
                    string = string.replace(v, random.choice(self.p[v]), 1)
                    break
        return string

    def classify_chomsky(self):
        is_type_3 = True  # Regular grammar
        is_type_2 = True  # Context-free grammar
        is_type_1 = True  # Context-sensitive grammar
        is_type_0 = True  # Unrestricted grammar (default)

        for left, right_rules in self.p.items():
            for right in right_rules:
                if len(left) > len(right):  # Context-sensitive check
                    is_type_1 = False
                if len(left) > 1 or not left.isupper():  # Context-free check
                    is_type_2 = False
                if len(right) > 2 or (len(right) == 2 and not right[0].islower()):
                    is_type_3 = False  # Regular grammar check

        if is_type_3:
            return "Type 3: Regular Grammar"
        elif is_type_2:
            return "Type 2: Context-Free Grammar"
        elif is_type_1:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"

    def to_finite_automaton(self):
        q = self.vn
        sigma = self.vt
        q0 = self.start_symbol
        delta = {}

        for key in self.p.keys():
            if key not in delta:
                delta[key] = {}

            for rule in self.p[key]:
                symbol = rule[0]
                next_state = rule[1] if len(rule) > 1 else None

                if symbol not in delta[key]:
                    delta[key][symbol] = set()
                delta[key][symbol].add(next_state)

        f = {key for key in self.p if all(rule in self.vt for rule in self.p[key])}
        f.add('C')

        return FiniteAutomaton(q, sigma, delta, q0, f)

    def finite_automaton_to_grammar(self, fa):
        grammar_rules = {}

        states = sorted(fa.q)
        state_mapping = {}

        if len(states) >= 1:
            state_mapping[states[0]] = 'S'
        if len(states) >= 2:
            state_mapping[states[1]] = 'A'
        if len(states) >= 3:
            state_mapping[states[2]] = 'B'
        if len(states) >= 4:
            state_mapping[states[3]] = 'C'

        for state in states:
            new_state_name = state_mapping.get(state, "")
            if new_state_name:
                grammar_rules[new_state_name] = []

                #add ε-production if the state is final
                if state in fa.f:
                    grammar_rules[new_state_name].append("ε")

                #transitions as grammar rules
                if state in fa.delta:
                    for symbol, next_states in fa.delta[state].items():
                        for next_state in next_states:
                            mapped_next_state = state_mapping.get(next_state, "")
                            grammar_rules[new_state_name].append(symbol + mapped_next_state)
        return grammar_rules