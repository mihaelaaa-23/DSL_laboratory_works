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

    def to_finite_automaton(self):
        q = self.vn  # states
        sigma = self.vt  # alphabet
        q0 = self.start_symbol  # start state
        delta = {}  # Transition func

        for key in self.p.keys():
            for rule in self.p[key]:
                if key not in delta:
                    delta[key] = []
                if len(rule) == 2:
                    delta[key].append((rule[0], rule[1]))  # (input symbol, next state)
                else:
                    delta[key].append((rule[0], None))  # terminal transition

        # find final states (terminal only strings)
        f = {key for key in self.p if all(rule in self.vt for rule in self.p[key])}
        f.add('C')  # C is final state

        return FiniteAutomaton(q, sigma, delta, q0, f)