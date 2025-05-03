class Node:
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class BinaryOpNode(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinaryOp({self.op.value}, {self.left}, {self.right})"


class UnaryOpNode(Node):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp({self.op.value}, {self.expr})"


class NumberNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Number({self.value})"


class VariableNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Variable({self.name})"


class AssignmentNode(Node):
    def __init__(self, variable, value):
        super().__init__()
        self.variable = variable
        self.value = value

    def __str__(self):
        return f"Assignment({self.variable}, {self.value})"


class FunctionCallNode(Node):
    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args

    def __str__(self):
        return f"Function({self.name}, {self.args})"


class AbsoluteValueNode(Node):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def __str__(self):
        return f"Abs({self.expr})"
