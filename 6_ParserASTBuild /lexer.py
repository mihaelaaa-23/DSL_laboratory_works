from tokenizer import Tokenizer, TokenType


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.set_current_char()

    def __str__(self):
        return f"Lexer({self.text})"

    def __repr__(self):
        return self.__str__()

    def set_current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self):
        self.pos += 1
        self.current_char = self.set_current_char()

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        if self.current_char == "-":  # handle negative numbers
            result += "-"
            self.advance()

        # at least one digit follows the "-" or start scanning a number
        if self.current_char is None or not self.current_char.isdigit():
            return Tokenizer(TokenType.MINUS, "-")  # If "-" is standalone, return it as a token

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            result += self.current_char
            self.advance()

        return Tokenizer(TokenType.NUMBER, float(result) if "." in result else int(result))

    def identifier(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        if result in {"sin", "cos", "tan", "cot", "exp", "sqrt"}:
            return Tokenizer(TokenType.FUNCTION, result)
        return Tokenizer(TokenType.IDENTIFIER, result)

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

    def tokenize(self):
        tokens = []
        while (token := self.get_next_token()).type != TokenType.EOF:
            tokens.append(token)
        tokens.append(token)
        return tokens
