from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    FACTORIAL = auto()
    MODULUS = auto()
    LPAREN = auto()
    RPAREN = auto()
    ASSIGN = auto()
    IDENTIFIER = auto()
    FUNCTION = auto()
    ABS_BAR = auto()
    EOF = auto()

    def __repr__(self):
        return self.name


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self, message):
        raise Exception(f"Lexer error: {message} at position {self.pos}")

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_number(self):
        result = ""
        has_decimal = False

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal:
                    self.error("Multiple decimal points in number")
                has_decimal = True
            result += self.current_char
            self.advance()

        try:
            return float(result) if has_decimal else int(result)
        except ValueError:
            self.error(f"Invalid number format: {result}")

    def parse_identifier(self):
        result = ""

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Check if it's a predefined function
        functions = {'sin', 'cos', 'tan', 'log', 'sqrt'}
        if result in functions:
            return Token(TokenType.FUNCTION, result)

        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return Token(TokenType.NUMBER, self.parse_number())

            if self.current_char.isalpha() or self.current_char == '_':
                identifier = self.parse_identifier()
                if isinstance(identifier, Token):  # It's a function
                    return identifier
                return Token(TokenType.IDENTIFIER, identifier)

            # Handle operators
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '^':
                self.advance()
                return Token(TokenType.POWER, '^')

            if self.current_char == '!':
                self.advance()
                return Token(TokenType.FACTORIAL, '!')

            if self.current_char == '%':
                self.advance()
                return Token(TokenType.MODULUS, '%')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=')

            if self.current_char == '|':
                self.advance()
                return Token(TokenType.ABS_BAR, '|')

            # If we get here, we have an unexpected character
            self.error(f"Unexpected character: {self.current_char}")

        return Token(TokenType.EOF, None)


class RegexLexer:
    def __init__(self, text):
        import re
        self.text = text
        self.tokens = []
        self.pos = 0

        # Define token patterns
        token_patterns = [
            ('NUMBER', r'\d+(\.\d+)?'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('POWER', r'\^'),
            ('FACTORIAL', r'!'),
            ('MODULUS', r'%'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('ASSIGN', r'='),
            ('ABS_BAR', r'\|'),
            ('FUNCTION', r'(sin|cos|tan|log|sqrt)(?=\()'),  # functions followed by '('
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('WHITESPACE', r'\s+')
        ]

        # Build the regex pattern
        pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
        self.regex = re.compile(pattern)

        # Tokenize the input
        self.tokenize()

    def tokenize(self):
        pos = 0
        while pos < len(self.text):
            match = self.regex.match(self.text, pos)
            if not match:
                raise Exception(f"Invalid token at position {pos}: {self.text[pos:]}")

            group = match.lastgroup
            if group != 'WHITESPACE':  # Skip whitespace
                value = match.group()
                token_type = getattr(TokenType, group)

                # Convert number strings to actual numbers
                if token_type == TokenType.NUMBER:
                    value = float(value) if '.' in value else int(value)

                self.tokens.append(Token(token_type, value))

            pos = match.end()

        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None))

    def get_next_token(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return Token(TokenType.EOF, None)


def tokenize(text, use_regex=False):
    lexer = RegexLexer(text) if use_regex else Tokenizer(text)
    tokens = []

    if use_regex:
        # RegexLexer has already tokenized the entire input
        tokens = lexer.tokens
    else:
        # CharacterLexer tokenizes one token at a time
        token = lexer.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = lexer.get_next_token()
        tokens.append(token)  # Add EOF token

    return tokens