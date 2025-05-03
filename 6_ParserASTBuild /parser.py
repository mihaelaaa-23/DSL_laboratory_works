from tokenizer import TokenType
from ast_nodes import (
    BinaryOpNode,
    UnaryOpNode,
    NumberNode,
    VariableNode,
    AssignmentNode,
    FunctionCallNode,
    AbsoluteValueNode
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def error(self, message):
        raise Exception(f"Parser error: {message} at position {self.pos}")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def peek(self, offset=1):
        peek_pos = self.pos + offset
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")

    def parse(self):
        if not self.tokens:
            return None

        result = self.expr()

        # Check if there are any tokens left
        if self.current_token and self.current_token.type != TokenType.EOF:
            self.error(f"Unexpected token: {self.current_token.type}")

        return result

    def expr(self):
        return self.assignment()

    def assignment(self):
        if (self.current_token and self.current_token.type == TokenType.IDENTIFIER and
                self.peek() and self.peek().type == TokenType.ASSIGN):
            var_name = self.current_token.value
            self.advance()  # consume the identifier
            self.advance()  # consume the '=' operator

            value = self.add_expr()  # parse the expression after '='
            return AssignmentNode(var_name, value)

        # otherwise, parse as an addition/subtraction expression
        return self.add_expr()

    def add_expr(self):
        node = self.mul_expr()

        while (self.current_token and
               self.current_token.type in (TokenType.PLUS, TokenType.MINUS)):
            op = self.current_token
            self.advance()
            right = self.mul_expr()
            node = BinaryOpNode(node, op, right)

        return node

    def mul_expr(self):
        node = self.pow_expr()

        while (self.current_token and
               self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULUS)):
            op = self.current_token
            self.advance()
            right = self.pow_expr()
            node = BinaryOpNode(node, op, right)

        return node

    def pow_expr(self):
        node = self.unary_expr()

        while self.current_token and self.current_token.type == TokenType.POWER:
            op = self.current_token
            self.advance()
            right = self.unary_expr()
            node = BinaryOpNode(node, op, right)

        return node

    def unary_expr(self):
        # Handle unary minus (like -5)
        if self.current_token and self.current_token.type == TokenType.MINUS:
            op = self.current_token
            self.advance()
            expr = self.factor()
            return UnaryOpNode(op, expr)

        # Parse regular factor
        node = self.factor()

        # Handle factorial
        if self.current_token and self.current_token.type == TokenType.FACTORIAL:
            op = self.current_token
            self.advance()
            return UnaryOpNode(op, node)

        return node

    def factor(self):
        token = self.current_token

        if not token:
            self.error("Unexpected end of input")

        if token.type == TokenType.NUMBER:
            self.advance()
            value = token.value.value if hasattr(token.value, 'value') else token.value
            return NumberNode(value)

        elif token.type == TokenType.IDENTIFIER:
            if self.peek() and self.peek().type == TokenType.LPAREN:
                return self.func_call()
            else:
                self.advance()
                return VariableNode(token.value)

        elif token.type == TokenType.FUNCTION:
            return self.func_call()

        elif token.type == TokenType.LPAREN:
            self.advance()  # consume '('
            node = self.add_expr()

            if not self.current_token:
                self.error("Unexpected end of input, expected ')'")

            if self.current_token.type != TokenType.RPAREN:
                self.error(
                    f"Expected ')', got {self.current_token.type} with value {getattr(self.current_token, 'value', 'unknown')}")

            self.eat(TokenType.RPAREN)  # consume ')'
            return node

        elif token.type == TokenType.ABS_BAR:
            self.advance()  # consume '|'
            expr = self.expr()
            self.eat(TokenType.ABS_BAR)  # consume '|'
            return AbsoluteValueNode(expr)

        else:
            self.error(f"Unexpected token: {token.type}")

    def func_call(self):
        # Parse function calls like sin(30)
        func_name = self.current_token.value
        self.advance()  # consume function name

        self.eat(TokenType.LPAREN)  # consume '('
        args = self.expr()
        self.eat(TokenType.RPAREN)  # consume ')'

        return FunctionCallNode(func_name, args)