import unittest
from grammar import Grammar

class TestFiniteAutomaton(unittest.TestCase):
    def test_string_belong_to_language(self):
        grammar = Grammar()
        finiteAutomaton = grammar.to_finite_automaton()

        self.assertFalse(finiteAutomaton.string_belongs_to_language('ab'))
        self.assertFalse(finiteAutomaton.string_belongs_to_language('bb'))
        self.assertTrue(finiteAutomaton.string_belongs_to_language('aabb'))
        self.assertTrue(finiteAutomaton.string_belongs_to_language('abaabb'))
        self.assertFalse(finiteAutomaton.string_belongs_to_language('baa'))


if __name__ == '__main__':
    unittest.main()
