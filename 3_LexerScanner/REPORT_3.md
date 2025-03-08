# Lexer & Scanner

### Course: Formal Languages & Finite Automata

### Author: Mihaela Untu | FAF-232

----

## Theory
Lexical analysis is a fundamental aspect of language processing, whether in the context of programming languages, domain-specific languages (DSLs), or any formal language. It involves the process of converting a sequence of characters into a sequence of tokens, which are the meaningful units of a language. These tokens typically represent identifiers, keywords, symbols, operators, and literals that conform to the syntax of the language being analyzed.

A lexer, also known as a scanner or tokenizer, is a fundamental component in the process of lexical analysis. Lexical analysis is the first step in interpreting or compiling a program. It involves breaking down a string of characters into meaningful chunks called tokens. These tokens are categorized based on predefined rules of the language being analyzed. 

Tokens are the building blocks of a language. They represent the smallest units of meaning, such as numbers, operators, or identifiers. The lexer processes the input text and produces a stream of tokens, which can then be used by a parser to understand the structure of the program.

## Objectives:
1. Understand the concept of lexical analysis.
2. Learn how a lexer/scanner/tokenizer works internally.
3. Implement a lexer that can tokenize mathematical expressions, including variables and functions.

**Note**: Just because too many students were showing me the same idea of lexer for a calculator, I've decided to specify requirements for such case. Try to make it at least a little more complex. Like, being able to pass integers and floats, also to be able to perform trigonometric operations (cos and sin). But it does not mean that you need to do the calculator, you can pick anything interesting you want


## Implementation description

### Token Types
First, I defined the types of tokens that the lexer will recognize. These are represented as an enumeration (`TokenType`). The tokens include numbers, identifiers (like variables), functions (like `sin`, `cos`, `tan`, `cot`), and various operators (like `+`, `-`, `*`, `/`).

```python
from enum import Enum

class TokenType(str, Enum):
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"  # variables like x, y
    FUNCTION = "FUNCTION"  # sin, cos, tan, cot
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULUS = "MODULUS"
    POWER = "POWER"
    FACTORIAL = "FACTORIAL"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    ABS_BAR = "ABS_BAR"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"
```

### Token Class
Next, I created a `Tokenizer` class to represent individual tokens. Each token has a type (from the `TokenType` enum) and a value (the actual character or number it represents).
The `Tokenizer` class is a simple data structure that holds the type and value of a token. The `__str__` and `__repr__` methods provide a readable string representation of the token, which is useful for debugging. The `__eq__` method allows comparing two tokens to check if they are equal, which is helpful for testing.
```python
class Tokenizer:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
```

### Lexer Class
The `Lexer` class is the core of the implementation. It processes the input text and generates tokens. Below are descriptions of the main methods:

- **`__init__`**: Initializes the lexer with the input text and sets the starting position and current character. It sets the starting position (`pos`) to `0` and calls `set_current_char` to set the current character being processed.
```python
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.set_current_char()
```

- **`set_current_char`**: Sets the current character based on the current position in the text. If the position is beyond the text length, it returns `None`, indicating the end of the input.
```python
    def set_current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
```

- **`advance`**: Moves the position forward and updates the current character. This is used to move through the input text character by character.
```python
    def advance(self):
        self.pos += 1
        self.current_char = self.set_current_char()
```

- **`skip_whitespace`**: This method skips any whitespace characters (like spaces or tabs) in the input text. It ensures that the lexer ignores unnecessary spaces and focuses on meaningful characters.
```python
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
```

- **`number`**: Processes numeric values, including negative numbers and floating-point numbers. It builds the number as a string and converts it to either an integer or a float. If a standalone "-" is encountered (without a following digit), it is treated as a `MINUS` token.
```python
    def number(self):
        result = ""
        if self.current_char == "-":  # handle negative numbers
            result += "-"
            self.advance()

        if self.current_char is None or not self.current_char.isdigit():
            return Tokenizer(TokenType.MINUS, "-") 

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            result += self.current_char
            self.advance()

        return Tokenizer(TokenType.NUMBER, float(result) if "." in result else int(result))
```

- **`identifier`**: Processes identifiers (like variable names) and functions (like `sin`, `cos`, `exp`, `sqrt`). It collects alphanumeric characters and underscores into a string. If the string matches a known function, it returns a `FUNCTION` token, otherwise, it returns an `IDENTIFIER` token.
```python
    def identifier(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        if result in {"sin", "cos", "tan", "cot", "exp", "sqrt"}:
            return Tokenizer(TokenType.FUNCTION, result)
        return Tokenizer(TokenType.IDENTIFIER, result)
```

- **`get_next_token`**: The main method of the lexer. It identifies the type of the next token in the input text and returns it. It handles numbers, identifiers, functions, operators, and unknown characters. If the end of the input is reached, it returns an `EOF` (End of File) token.
```python
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit() or self.current_char == "-":  # Handle negative numbers
                return Tokenizer(TokenType.NUMBER, self.number())
            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == "|":
                self.advance()
                return Tokenizer(TokenType.ABS_BAR, "|")

            if self.current_char == "+":
                self.advance()
                return Tokenizer(TokenType.PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Tokenizer(TokenType.MINUS, "-")
            if self.current_char == "*":
                self.advance()
                return Tokenizer(TokenType.MULTIPLY, "*")
            if self.current_char == "/":
                self.advance()
                return Tokenizer(TokenType.DIVIDE, "/")
            if self.current_char == "%":
                self.advance()
                return Tokenizer(TokenType.MODULUS, "%")
            if self.current_char == "^":
                self.advance()
                return Tokenizer(TokenType.POWER, "^")
            if self.current_char == "!":
                self.advance()
                return Tokenizer(TokenType.FACTORIAL, "!")
            if self.current_char == "(":
                self.advance()
                return Tokenizer(TokenType.LPAREN, "(")
            if self.current_char == ")":
                self.advance()
                return Tokenizer(TokenType.RPAREN, ")")
            if self.current_char == "=":
                self.advance()
                return Tokenizer(TokenType.ASSIGN, "=")

            # Unknown character handling
            unknown = self.current_char
            self.advance()
            return Tokenizer(TokenType.UNKNOWN, unknown)

        return Tokenizer(TokenType.EOF, None)
```

- **`tokenize`**: The method repeatedly calls `get_next_token` to generate a list of tokens until the end of the input is reached. It returns the complete list of tokens, which represents the processed input text.
```python
    def tokenize(self):
        tokens = []
        while (token := self.get_next_token()).type != TokenType.EOF:
            tokens.append(token)
        tokens.append(token)
        return tokens
```

## Conclusions / Screenshots / Results
In this laboratory work, I implemented a lexer capable of tokenizing mathematical expressions, including variables, functions, and various operators. The lexer processes the input text and generates a list of tokens, each representing a meaningful part of the expression. This implementation lays the groundwork for further steps in building a compiler or interpreter, such as parsing and evaluation.

### Results
For the following main.py program, we get the results below the program:
```python
from lexer import Lexer

print("Running Lexer Tests")
test_expressions = [
    "3.14",
    "x = exp(2) + sqrt(5)",
    "x = |5| + |cos(-30)|",
    "x = 5+3 * 2",
    "y = -4.5 / 2 + sin(30)",
    "z = cos(60) * tan(45) - 7!",
    "a = 2^3 % 4",
    "b = cot(90) + 15",
    "c = (5 + 2) * 3 / 7"
]

for expr in test_expressions:
    print(f"\nExpression: {expr}")
    lexer = Lexer(expr)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
```

```python
Running Lexer Tests

Expression: 3.14
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 3.14))
Token(TokenType.EOF, None)

Expression: x = exp(2) + sqrt(5)
Token(TokenType.IDENTIFIER, x)
Token(TokenType.ASSIGN, =)
Token(TokenType.FUNCTION, exp)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 2))
Token(TokenType.RPAREN, ))
Token(TokenType.PLUS, +)
Token(TokenType.FUNCTION, sqrt)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 5))
Token(TokenType.RPAREN, ))
Token(TokenType.EOF, None)

Expression: x = |5| + |cos(-30)|
Token(TokenType.IDENTIFIER, x)
Token(TokenType.ASSIGN, =)
Token(TokenType.ABS_BAR, |)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 5))
Token(TokenType.ABS_BAR, |)
Token(TokenType.PLUS, +)
Token(TokenType.ABS_BAR, |)
Token(TokenType.FUNCTION, cos)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, -30))
Token(TokenType.RPAREN, ))
Token(TokenType.ABS_BAR, |)
Token(TokenType.EOF, None)

Expression: x = 5+3 * 2
Token(TokenType.IDENTIFIER, x)
Token(TokenType.ASSIGN, =)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 5))
Token(TokenType.PLUS, +)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 3))
Token(TokenType.MULTIPLY, *)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 2))
Token(TokenType.EOF, None)

Expression: y = -4.5 / 2 + sin(30)
Token(TokenType.IDENTIFIER, y)
Token(TokenType.ASSIGN, =)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, -4.5))
Token(TokenType.DIVIDE, /)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 2))
Token(TokenType.PLUS, +)
Token(TokenType.FUNCTION, sin)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 30))
Token(TokenType.RPAREN, ))
Token(TokenType.EOF, None)

Expression: z = cos(60) * tan(45) - 7!
Token(TokenType.IDENTIFIER, z)
Token(TokenType.ASSIGN, =)
Token(TokenType.FUNCTION, cos)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 60))
Token(TokenType.RPAREN, ))
Token(TokenType.MULTIPLY, *)
Token(TokenType.FUNCTION, tan)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 45))
Token(TokenType.RPAREN, ))
Token(TokenType.NUMBER, Token(TokenType.MINUS, -))
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 7))
Token(TokenType.FACTORIAL, !)
Token(TokenType.EOF, None)

Expression: a = 2^3 % 4
Token(TokenType.IDENTIFIER, a)
Token(TokenType.ASSIGN, =)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 2))
Token(TokenType.POWER, ^)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 3))
Token(TokenType.MODULUS, %)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 4))
Token(TokenType.EOF, None)

Expression: b = cot(90) + 15
Token(TokenType.IDENTIFIER, b)
Token(TokenType.ASSIGN, =)
Token(TokenType.FUNCTION, cot)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 90))
Token(TokenType.RPAREN, ))
Token(TokenType.PLUS, +)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 15))
Token(TokenType.EOF, None)

Expression: c = (5 + 2) * 3 / 7
Token(TokenType.IDENTIFIER, c)
Token(TokenType.ASSIGN, =)
Token(TokenType.LPAREN, ()
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 5))
Token(TokenType.PLUS, +)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 2))
Token(TokenType.RPAREN, ))
Token(TokenType.MULTIPLY, *)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 3))
Token(TokenType.DIVIDE, /)
Token(TokenType.NUMBER, Token(TokenType.NUMBER, 7))
Token(TokenType.EOF, None)
```

## References
1. [Lexical Analysis](https://en.wikipedia.org/wiki/Lexical_analysis)
2. [Python Documentation](https://www.python.org/doc/)