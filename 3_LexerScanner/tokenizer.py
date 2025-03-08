from enum import Enum


class TokenType(str, Enum):
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"  # variables like x, y
    FUNCTION = "FUNCTION"  # sin, cos, tan, cot, exp, sqrt
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
