import re
from tokenizer import Tokenizer, TokenType


class RegexLexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0

        # Define token patterns using regular expressions
        self.token_patterns = [
            # Numbers (integers and floats, with optional negative sign)
            (r'-?\d+\.\d+', lambda v: Tokenizer(TokenType.NUMBER, float(v))),
            (r'-?\d+', lambda v: Tokenizer(TokenType.NUMBER, int(v))),

            # Functions
            (r'(sin|cos|tan|cot|exp|sqrt)', lambda v: Tokenizer(TokenType.FUNCTION, v)),

            # Identifiers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', lambda v: Tokenizer(TokenType.IDENTIFIER, v)),

            # Operators
            (r'\+', lambda v: Tokenizer(TokenType.PLUS, v)),
            (r'-', lambda v: Tokenizer(TokenType.MINUS, v)),
            (r'\*', lambda v: Tokenizer(TokenType.MULTIPLY, v)),
            (r'/', lambda v: Tokenizer(TokenType.DIVIDE, v)),
            (r'%', lambda v: Tokenizer(TokenType.MODULUS, v)),
            (r'\^', lambda v: Tokenizer(TokenType.POWER, v)),
            (r'!', lambda v: Tokenizer(TokenType.FACTORIAL, v)),
            (r'\|', lambda v: Tokenizer(TokenType.ABS_BAR, v)),

            # Parentheses
            (r'\(', lambda v: Tokenizer(TokenType.LPAREN, v)),
            (r'\)', lambda v: Tokenizer(TokenType.RPAREN, v)),

            # Assignment
            (r'=', lambda v: Tokenizer(TokenType.ASSIGN, v)),

            # Whitespace (to be skipped)
            (r'\s+', None)
        ]

    def tokenize(self):
        tokens = []
        remaining_text = self.text

        # Process the text until it's all consumed
        while remaining_text:
            match_found = False

            # Try each pattern
            for pattern, token_generator in self.token_patterns:
                regex = re.compile('^' + pattern)
                match = regex.match(remaining_text)

                if match:
                    matched_text = match.group(0)

                    # Skip whitespace
                    if token_generator is None:
                        remaining_text = remaining_text[len(matched_text):]
                        match_found = True
                        break

                    # Create and add the token
                    token = token_generator(matched_text)
                    tokens.append(token)

                    # Update remaining text
                    remaining_text = remaining_text[len(matched_text):]
                    match_found = True
                    break

            # If no patterns matched, handle the error
            if not match_found:
                unknown_char = remaining_text[0]
                tokens.append(Tokenizer(TokenType.UNKNOWN, unknown_char))
                remaining_text = remaining_text[1:]

        # Add EOF token
        tokens.append(Tokenizer(TokenType.EOF, None))

        return tokens