class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q  # states
        self.sigma = sigma  # alphabet
        self.delta = delta  # transition func
        self.q0 = q0  # start state
        self.f = f  # accept states

    def string_belongs_to_language(self, input_string):
        current_state = self.q0

        for c in input_string:
            if c not in self.sigma or current_state not in self.delta:
                return False

            next_state = None
            for transition in self.delta[current_state]:
                if c == transition[0]:  # if the transition matches input
                    next_state = transition[1] if transition[1] is not None else current_state
                    break

            if next_state is None:
                return False  # no valid transition

            current_state = next_state

        return current_state in self.f

