# Chomsky Normal Form

### Course: Formal Languages & Finite Automata  
### Author: Mihaela Untu | FAF-232 | Variant 28

---

## Theory

In formal language theory, a **context-free grammar (CFG)** is in **Chomsky Normal Form (CNF)** if each of its production rules is of one of the following forms:

- A → BC  
- A → a  
- S → ε (only if ε ∈ L(G))

Where A, B, and C are non-terminal symbols, *a* is a terminal symbol, and S is the start symbol. Also, B and C must not be the start symbol, and the ε-rule is allowed only for the start symbol under specific conditions.

---

## Objectives

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
   1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
   2. The implemented functionality needs executed and tested.
   3. Also, another **BONUS point** would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.
---

## Implementation Description

The entire CNF conversion logic was implemented in the `Grammar` class. The process is divided into a well-structured sequence of transformation steps. Each of these transformations is encapsulated in a distinct method to enhance clarity, reusability, and testing capabilities.

Below are the steps followed in the CNF conversion:

### 1. Eliminating ε-productions

The goal of this step is to eliminate productions that generate the empty string `ε`. The method scans for nullable non-terminals and generates new equivalent productions without the nullable symbols using a helper function `_expand_nullable_prod`.

```python
    def eliminate_epsilon_productions(self):
        nullable = set()

        # find all nullable non-terminals
        for non_terminal in self.non_terminals:
            for production in self.rules[non_terminal]:
                if production == "ε":
                    nullable.add(non_terminal)

        # check for indirect nullable non-terminals
        changes = True
        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                if non_terminal not in nullable:
                    for production in self.rules[non_terminal]:
                        if all(symbol in nullable for symbol in production):
                            nullable.add(non_terminal)
                            changes = True
                            break

        # eliminate epislon-productions
        new_rules = {}
        for non_terminal in self.rules:
            new_prods = []
            for production in self.rules[non_terminal]:
                if production != "ε":
                    new_prods.extend(
                        self._expand_nullable_prod(production, nullable))
            # remove duplicates
            new_rules[non_terminal] = list(set(new_prods))

        self.rules = new_rules
```

The `_expand_nullable_prod` method generates all possible production combinations by removing nullable symbols:

```python
    def _expand_nullable_prod(self, production, nullable):
        expansions = ['']

        for symbol in production:
            new_expansions = []
            if symbol in nullable:
                for expansion in expansions:
                    new_expansions.append(expansion + symbol)
                    new_expansions.append(expansion)
            else:
                for expansion in expansions:
                    new_expansions.append(expansion + symbol)
            expansions = new_expansions

        return [expansion for expansion in expansions if expansion]
```

For example:  
`_expand_nullable_prod("ABC", {'B'})` → `["AC", "ABC"]`

### 2. Eliminating Renaming (Unit) Productions

Renaming rules are of the form A → B where both A and B are non-terminals. These rules are recursively replaced by directly copying B's productions to A and removing the renaming rule.

```python
    def eliminate_renaming(self):
        # track changes to avoid re-processing unit productions
        changes = True
        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                # filter out unit productions
                unit_productions = [
                    p for p in self.rules[non_terminal] if p in self.non_terminals]
                for unit in unit_productions:
                    # add the productions of the unit non-terminal, replacing the unit production
                    new_productions = self.rules[unit]
                    if new_productions:
                        self.rules[non_terminal].extend(new_productions)
                        self.rules[non_terminal].remove(unit)
                        # make sure to remove any duplicates
                        self.rules[non_terminal] = list(
                            set(self.rules[non_terminal]))
                        changes = True

                # after processing the unit productions for a non-terminal, filter them out
                self.rules[non_terminal] = [
                    p for p in self.rules[non_terminal] if p not in self.non_terminals]
```

This method makes use of a loop with a `changes` flag to make sure that indirect chains of unit productions are resolved.

### 3. Eliminating Inaccessible Symbols

This step ensures that only the symbols reachable from the start symbol are preserved in the grammar. Inaccessible symbols and their associated rules are removed.

```python
    def eliminate_inaccessible_symbols(self):
        accessible = {self.start}
        changes = True  # Flag to check if there were changes in the last iteration
        old_rules = self.rules.copy()

        while changes:
            changes = False
            for non_terminal in accessible.copy():
                for production in self.rules[non_terminal]:
                    for symbol in production:
                        if symbol in self.non_terminals and symbol not in accessible:
                            accessible.add(symbol)
                            changes = True

        self.non_terminals = list(accessible)
        self.rules = {nt: old_rules[nt] for nt in accessible}
```

The method builds a set of accessible non-terminals and reconstructs the rules based on it.

### 4. Eliminating Non-Productive Symbols

Non-productive symbols are those that do not lead to any terminal strings. This method filters out such symbols and their productions, ensuring that every rule contributes to the derivation of valid strings.

```python
    def eliminate_non_productive_symbols(self):
        productive = {self.start}
        changes = True

        while changes:
            changes = False
            for non_terminal in self.non_terminals:
                if non_terminal not in productive:
                    for production in self.rules[non_terminal]:
                        if all(symbol in self.terminals or symbol in productive for symbol in production):
                            productive.add(non_terminal)
                            changes = True
                            break

        self.non_terminals = list(productive)

        # Create a new dictionary to store the updated rules
        updated_rules = {}
        for nt in productive:
            productive_rules = []

            for production in self.rules[nt]:
                if all(symbol in self.terminals or symbol in productive for symbol in production):
                    productive_rules.append(production)

            updated_rules[nt] = productive_rules

        self.rules = updated_rules
```

It starts by assuming the start symbol is productive and iteratively adds new productive symbols based on their derivations.

### 5. Converting to CNF

This final step ensures that:
- All productions are either of the form A → a or A → BC.
- All right-hand sides with more than two symbols are broken down into binary rules using newly generated non-terminals.
- Terminal symbols in binary rules are replaced with new non-terminals that map directly to the terminals.

**Step 1: Eliminate epsilon-productions**

In this step, I remove rules like `A → ε`, which means a non-terminal can produce the empty string.
First, I collect all non-terminals that can eventually become ε (directly or indirectly). Then, I go through all the 
rules and add new ones by imagining what happens if those ε-symbols just disappear.

Example: if `X → AB` and `B → ε`, I add `X → A` as an option too.
```python
    def to_cnf(self, print_steps=True):
        if self.is_cnf():
            return

        self.eliminate_epsilon_productions()
        if print_steps:
            print('1. After eliminating epsilon productions:')
            self.print_rules()
            print()
            
```

**Step 2: Eliminate renaming/unit-productions**

Now I remove rules where one non-terminal just points to another, like `A → B`.
Instead of going through `A → B → something`, I copy all of `B`'s rules directly to `A`, and delete the rule `A → B`.
In the end, every rule will either produce terminals or combinations, not just a single other non-terminal.
```python
        self.eliminate_renaming()
        if print_steps:
            print('2. After eliminating renaming productions:')
            self.print_rules()
            print()
```

**Step 3: Eliminate inaccessible symbols**

This step gets rid of non-terminals that can never be reached from the start symbol (`S`).
I simulate starting from `S` and collect all symbols that can be reached through the rules. Everything else is deleted, 
because it’s useless in generating any string.
```python
        self.eliminate_inaccessible_symbols()
        if print_steps:
            print('3. After eliminating inaccessible symbols:')
            self.print_rules()
            print()
```

**Step 4: Eliminate non-productive symbols**

Now I remove symbols that will never lead to a string made of only terminals.
I keep only the symbols that are "productive", meaning they can eventually turn into something real (like `a`, `b`, etc.). 
If a rule leads nowhere meaningful, I remove it.
```python
       self.eliminate_non_productive_symbols()
       if print_steps:
           print('4. After eliminating non-productive symbols:')
           self.print_rules()
           print()
```

**Step 5: Convert to CNF**

In the final step, I make sure every rule fits CNF format:
- either one terminal (like `A → a`)
- or two non-terminals (like `A → BC`)

If a rule has more than 2 symbols on the right (like `A → BCD`), I break it into binary chunks using new non-terminals. 
Example: `A → BCD` becomes `A → BX`, then `X → CD`.
If there’s a mix of terminal and non-terminal (like `A → aB`), I replace the terminal with a new non-terminal, like:
`1 → a` and `A → 1B`.
At the end, I rebuild the rule set with all the original and new non-terminals.
```python
        rhs_to_non_terminal = {}
        old_non_terminals = list(self.rules)

        new_rules = {}
        for non_terminal in list(self.rules):
            new_rules[non_terminal] = set()
            for production in self.rules[non_terminal]:
                # Case for productions with more than 2 symbols
                while len(production) > 2:
                    # Extract the first two symbols
                    first_two_symbols = production[:2]

                    if first_two_symbols in rhs_to_non_terminal:
                        new_non_terminal = rhs_to_non_terminal[first_two_symbols]
                    else:
                        new_non_terminal = self._create_new_non_terminal()
                        new_rules[new_non_terminal] = {first_two_symbols}
                        rhs_to_non_terminal[first_two_symbols] = new_non_terminal
                    # Replace the first two symbols with the new non-terminal
                    production = new_non_terminal + production[2:]

                new_rules[non_terminal].add(production)

        # Handle mixed productions
        for non_terminal, productions in list(new_rules.items()):
            temp_productions = productions.copy()
            for production in temp_productions:
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    new_production = []
                    for symbol in production:
                        if symbol in self.terminals:
                            if symbol in rhs_to_non_terminal:
                                new_non_terminal = rhs_to_non_terminal[symbol]
                            else:
                                new_non_terminal = self._create_new_non_terminal()
                                new_rules[new_non_terminal] = {symbol}
                                rhs_to_non_terminal[symbol] = new_non_terminal
                            new_production.append(new_non_terminal)
                        else:
                            new_production.append(symbol)
                    productions.remove(production)
                    productions.add(''.join(new_production))

        # Reorder the rules to match the original order + new non-terminals
        self.rules = {nt: new_rules[nt] for nt in old_non_terminals +
                      list(set(new_rules) - set(old_non_terminals))}

        if print_steps:
            print('5. After converting to CNF:')
            self.print_rules()
            print()
```

An internal method `_create_new_non_terminal` generates unique non-terminal names to avoid conflicts:

```python
    def _create_new_non_terminal(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZαβγδζηθικλμνξοπρστυφχψω'

        for letter in alphabet:
            if letter not in self.non_terminals:
                self.non_terminals.append(letter)
                return letter

        for letter in alphabet:
            for num in range(100):
                new_symbol = f'{letter}{num}'
                if new_symbol not in self.non_terminals:
                    self.non_terminals.append(new_symbol)
                    return new_symbol

        raise ValueError("Exhausted all possible non-terminal symbols.")
```

This method uses a pool of Greek and Latin characters and falls back to appending numbers if needed.

---

## Testing & Validation

To ensure correctness, a suite of unit tests was written using `unittest`. The tests check the integrity of the grammar 
at each step and validate the final CNF format. The variant used for testing is number **28**, with the following 
initial grammar:

```python
non_terminals = ['S', 'A', 'B', 'C', 'D', 'X']
terminals = ['a', 'b']
rules = {
    'S': ['B'],
    'A': ['aX', 'bX'],
    'X': ['BX', 'b', 'ε'],
    'B': ['AXaD'],
    'D': ['a', 'aD'],
    'C': ['Ca']
}
```

Some of the test methods include:

This test validates the correct removal of ε-productions from the grammar. After calling the 
`eliminate_epsilon_productions` method, the test asserts that the `ε` symbol no longer appears in the productions of 
non-terminal `X`.
```python
    def test_eliminate_epsilon_productions(self):
        self.grammar.eliminate_epsilon_productions()
        self.assertNotIn('ε', self.grammar.rules['X'])
```

This is a comprehensive end-to-end test that applies all transformation steps by invoking the `to_cnf` method and then 
performs structural validation of the resulting grammar. Specifically, it asserts the following conditions:

- Each production must have a length of at most 2 symbols.

- If a production has 2 symbols, both must be non-terminals.

- If a production has 1 symbol, it must be a terminal or ε.
```python
    def test_to_cnf(self):
        self.grammar.to_cnf(print_steps=True)
        for nt, prods in self.grammar.rules.items():
            for prod in prods:
                self.assertTrue(len(prod) <= 2)
                if len(prod) == 2:
                    self.assertTrue(
                        all(symbol in self.grammar.non_terminals for symbol in prod))
                if len(prod) == 1:
                    self.assertTrue(
                        prod in self.grammar.terminals or prod == 'ε')
```

Each test confirms that:
- ε-productions are removed
- Unit rules are eliminated
- Symbols are productive and accessible
- The grammar conforms to CNF: each production is of length 1 (with terminal) or 2 (with non-terminals only)

---

## Results

```doctest
Testing started at 10:23 ...


Ran 7 tests in 0.001s

OK
Launching unittests with arguments python -m unittest /Users/mihaela/Documents/UNIVERSITY/DSL_laboratory_works/5_ChomskyNormalForm/test.py in /Users/mihaela/Documents/UNIVERSITY/DSL_laboratory_works/5_ChomskyNormalForm

1. After eliminating epsilon productions:
S -> B
A -> a | aX | b | bX
B -> AXaD | AaD
C -> Ca
D -> a | aD
X -> B | BX | b

2. After eliminating renaming productions:
S -> AXaD | AaD
A -> a | aX | b | bX
B -> AXaD | AaD
C -> Ca
D -> a | aD
X -> AXaD | AaD | BX | b

3. After eliminating inaccessible symbols:
S -> AXaD | AaD
A -> a | aX | b | bX
B -> AXaD | AaD
D -> a | aD
X -> AXaD | AaD | BX | b

4. After eliminating non-productive symbols:
S -> AXaD | AaD
A -> a | aX | b | bX
B -> AXaD | AaD
D -> a | aD
X -> AXaD | AaD | BX | b

5. After converting to CNF:
S -> 0D | 2D
A -> 3X | 4X | a | b
B -> 0D | 2D
D -> 3D | a
X -> 0D | 2D | BX | b
0 -> A3
1 -> AX
2 -> 13
3 -> a
4 -> b


Process finished with exit code 0

```
---

## Conclusion

In this lab, I implemented a class-based approach for transforming a context-free grammar into Chomsky Normal Form. Each step was modularized for clarity and testability. The final solution is capable of handling arbitrary grammars, not just a fixed example. The implementation passed all unit tests, validating its correctness. Although further improvements are possible, the current structure provides a strong base for extending CNF-related features.

---

## References

- [Chomsky Normal Form - Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)
- [Neso Academy - CNF Conversion](https://www.youtube.com/watch?v=FNPSlnj3Vt0&ab_channel=NesoAcademy)