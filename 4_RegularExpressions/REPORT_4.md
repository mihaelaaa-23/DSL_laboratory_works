
# Regular Expressions

### Course: Formal Languages & Finite Automata  
### Author: Mihaela Untu | FAF-232

---

## Theory

Regular expressions (regex) are a powerful formalism used to describe and match patterns in strings. They form the backbone of many parsing and lexical analysis techniques in compilers, search engines, and text-processing tools. In formal language theory, regular expressions define the class of regular languages, which can be recognized by finite automata.

A regular expression uses a combination of **symbols**, **operators**, and **quantifiers** to describe a language. Symbols are literal characters (like `a`, `b`, `1`, `x`), and operators include concatenation, union (`|`), Kleene star (`*`), and positive closure (`+`). Parentheses are used for grouping, allowing more complex expressions to be constructed.

The purpose of this lab work is to:
1. Understand how regular expressions are processed.
2. Build a tool to generate **valid strings** for given regexes.
3. Provide **step-by-step explanations** for how these expressions are interpreted.

---

## Objectives

1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown).

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. Bonus point: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

Write a good report covering all performed actions and faced difficulties.

---

## Regular Expressions (Variant 4)

![img.png](images/v4.png)

The regular expressions chosen for generation and analysis are:

1. `(S|T)(U|V)W*Y+24`
2. `L(M|N)O{3}P*Q(2|3)`
3. `R*S(T|U|V)W(X|Y|Z){2}`

Each expression defines a set of strings that follow a specific structure involving character choices, repetitions, and fixed suffixes. Our task is to **generate all matching strings** with a limited number of repetitions and explain how they are interpreted.

---

## Implementation Description

### `patterns.py`

`RegexPatterns` is a simple container class meant to store multiple regex pattern variants. Even though it only holds static data, wrapping it inside a class helps organize the code and group related constants together. 

`VARIANT_4` is a dictionary (key-value mapping) that holds three regex patterns. Each key (like `"regex_1"`) is a label for a particular regular expression, and the value is a string that represents the regex pattern. The `r` prefix (e.g., `r"(S|T)...`) indicates a raw string literal. In Python, raw strings treat backslashes (``) as literal characters, which is important for regex syntax — otherwise, Python would interpret backslashes as escape characters.
```python
class RegexPatterns:
    VARIANT_4 = {
        "regex_1": r"(S|T)(U|V)W*Y+24",
        "regex_2": r"L(M|N)O{3}P*Q(2|3)",
        "regex_3": r"R*S(T|U|V)W(X|Y|Z){2}"
    }
```

---

### `generator.py`

The `generator.py` file contains the Generator class which is responsible for parsing regular expressions and generating valid strings that match them. The implementation now handles regex parsing dynamically rather than using hardcoded patterns.
It processes groups `( )` with alternatives `|`, handles quantifiers `*`, `+`, `?`, and `{n}`, limits repetitions to 5 for unbounded quantifiers, and generates random valid strings

`__init__(self, expr)` initializes the `Generator` class with an expression string. The expression defines the pattern for generating random strings.
```python
    def __init__(self, expr):
        self.expr = expr
        self.chars = []
```
`generate_string(self)` parses the expression and generates a random string based on the defined patterns. It supports:
- Parentheses `()` for grouping with the `|` (OR) operator.
- `*` for 0 to 5 repetitions of the preceding character/group.
- `+` for 1 to 5 repetitions of the preceding character/group.
- `?` for 0 or 1 repetition of the preceding character/group.
- `^N` or `{N}` for exactly N repetitions of the preceding character/group.

```python
    def generate_string(self):
        string = []
        i = 0

        while i < len(self.expr):
            char = self.expr[i]

            if char == "(":
                group_end = self.expr.find(")", i)
                group_content = self.expr[i + 1:group_end]
                selected = self.generate_group(group_content)
                string.append(selected)
                i = group_end

            elif char == "*":
                last = string.pop()
                string.append(last * random.randint(0, 5))

            elif char == "+":
                last = string.pop()
                string.append(last * random.randint(1, 5))

            elif char == "^":
                repeat = int(self.expr[i + 1])
                last = string.pop()
                string.append(last * repeat)
                i += 1

            elif char == "?":
                last = string.pop()
                string.append(last * random.randint(0, 1))

            elif char == "{" and i + 2 < len(self.expr) and self.expr[i + 2] == "}":
                repeat = int(self.expr[i + 1])
                last = string.pop()
                string.append(last * repeat)
                i += 2

            elif char in {"|", ")", "}"}:
                pass

            else:
                string.append(char)

            i += 1

        return ' '.join(string)
```
`generate_group(self, group_expr)` handles expressions inside parentheses `()`, which define alternative options separated by `|`. Randomly selects one of the options and returns it.

```python
    def generate_group(self, group_expr):
        options = group_expr.split("|")
        return random.choice(options)
```

`generate_n_strings(self)` generates and prints five random strings using the generate_string method.
```python
    def generate_n_strings(self):
        for _ in range(5):
            print(self.generate_string())
```
---

### `main.py`

The `main.py` file serves as the entry point of the regular expression generator program. Its primary function is to coordinate the generation of valid strings from regex patterns and to display their structure and examples in a readable format. It brings together the main components of the project—pattern definitions, the generator logic, and the step-by-step explanation of each expression.
```python
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
```

---

## Results

Running the script on the three expressions produces different sets of valid strings. Below are example outputs with screenshots:

### Regex 1 `(S|T)(U|V)W*Y+24`
![img.png](images/RE1.png)
---

### Regex 2 `L(M|N)O{3}P*Q(2|3)`
![img_1.png](images/RE2.png)
---

### Regex 3 `R*S(T|U|V)W(X|Y|Z){2}`
![img_2.png](images/RE3.png)
---

## Conclusions

In this lab, the generation of valid strings from regular expressions was analyzed and implemented. We built a modular Python tool that interprets regex definitions, generates matching strings up to a bounded depth, and explains the internal processing steps for each pattern. This lab helped solidify our understanding of regular languages and gave us a hands-on approach to working with regex in a theoretical and practical context.

---

## References

1. [Regular Expressions - Wikipedia](https://en.wikipedia.org/wiki/Regular_expression)  
2. [Formal Language Theory](https://en.wikipedia.org/wiki/Formal_language)  
3. [Python Regex Tutorial (Built-in Syntax)](https://docs.python.org/3/library/re.html)
